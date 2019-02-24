from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.contrib.messages import SUCCESS, ERROR, get_messages
from django.contrib import messages
from .forms import UserCreateForm
from csesa_telegram.settings import SEND_TO_CHAT_ID, CHANNEL_USER_NAME
from .bot_utils import bot
from pprint import pprint



# Create your views here.


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class PostDetailView(DetailView):
    model = Post


def send_in_bot(msg, request):
    # if msg.image is not None:
    #     print('done')
    # print(msg.file)
    # print(msg.image)
    if 'file' not in request.POST.keys():
        if request.POST['content'] != "":
            tel_id = bot.sendDocument(SEND_TO_CHAT_ID, msg.file,
                                      caption=str(msg.author) + ': \n' + str(msg.content))
        else:
            tel_id = bot.sendDocument(SEND_TO_CHAT_ID, msg.file,
                                      caption=str(msg.author))

    elif 'image' not in request.POST.keys():
        if request.POST['content'] != "":
            tel_id = bot.sendPhoto(SEND_TO_CHAT_ID, msg.image,
                                   caption=str(msg.author) + ': \n' + str(msg.content))
        else:
            tel_id = bot.sendDocument(SEND_TO_CHAT_ID, msg.image,
                                      caption=msg.author)
    else:
        tel_id = bot.sendMessage(SEND_TO_CHAT_ID, str(msg.author) + ': \n' + str(msg.content))
    return tel_id['message_id']
    # pprint(tel_id)
    # print(tel_id['message_id'])
    #
    # post = Post.objects.last()
    # print(post)
    # post.telegram_id = str(tel_id['message_id'])
    # Post.objects.last().update(telegram_id=tel_id['message_id'])
    # post.save()
    # print(post.telegram_id)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = UserCreateForm
    template_name = 'blog/post_form.html'

    # fields = ['title', 'content', 'image']
    #
    def form_valid(self, form):
        #     # print(self.request.body.decode().title())
        #     # print(self.request.user)
        # print(self.request.FILES)

        ########################################################################
        flag = True
        # check for image in posts
        # if "image" in self.request.POST.keys():
        #     flag = False
        #
        # if self.request.POST['content'] != "":
        #     flag = True
        #
        # if 'file' in self.request.POST.keys():
        #     flag = False
        #
        # else:
        #     flag = flag or False

        if "image" in self.request.POST.keys() and self.request.POST[
            'content'] == "" and 'file' in self.request.POST.keys():
            flag = False

        if not flag:
            # return HttpResponse('invlkan')
            return render(self.request, 'blog/error.html')
        ########################################################################

        form.instance.author = self.request.user
        form.instance.image = self.request.FILES.get('image')
        form.instance.file = self.request.FILES.get('file')
        form.instance.telegram_id = send_in_bot(form.instance, self.request)

        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image', 'file']

    def edit_in_telegram(self, tel_id, content, if_file):
        if if_file:
            bot.editMessageCaption((CHANNEL_USER_NAME, tel_id), caption=content)
        else:
            # print(tel_id)
            bot.editMessageText((CHANNEL_USER_NAME, tel_id), text=content)

    def form_valid(self, form):
        form.instance.author = self.request.user
        super().form_valid(form)
        post = self.get_object()
        self.edit_in_telegram(post.telegram_id, post.content, post.image != '' or post.file != '')
        return super().form_valid(form)


    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    success_url = '/messenger/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def delete_telegram_post(self):
        post = self.get_object()
        id = post.telegram_id
        bot.deleteMessage((CHANNEL_USER_NAME, id))
        return True

    def delete(self, request, *args, **kwargs):
        self.delete_telegram_post()
        return super(PostDeleteView, self).delete(request)


def ContactView(request):
    return render(request, 'blog/contact.html')


class Logout(auth_views.LogoutView):
    def get(self, request, *args, **kwargs):
        super(Logout, self).get(request)
        return redirect('login')
