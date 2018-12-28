from django.shortcuts import render
from django.db import transaction
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse
from django.views import View

# Create your views here.
from csesa.settings import SEND_TO_CHAT_ID
from csesa.bot_utils import bot


class send_message(View):
    template_name = 'send_message.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, self.template_name, {'message': ''})
        else:
            return redirect(reverse('users:login') + "?next=" + request.path_info)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if 'file' in request.FILES:
                if request.POST['file_caption']:
                    bot.sendDocument(SEND_TO_CHAT_ID, request.FILES['file'],
                                     caption=request.user.last_name + ': \n' + request.POST['file_caption'])
                else:
                    bot.sendDocument(SEND_TO_CHAT_ID, request.FILES['file'],
                                     caption=request.user.last_name)

            elif 'image' in request.FILES:
                if request.POST['image_caption']:
                    bot.sendPhoto(SEND_TO_CHAT_ID, request.FILES['image'],
                              caption=request.user.last_name + ': \n' + request.POST['image_caption'])
                else:
                    bot.sendDocument(SEND_TO_CHAT_ID, request.FILES['image'],
                              caption=request.user.last_name)
            else:
                bot.sendMessage(SEND_TO_CHAT_ID, request.user.last_name + ': \n' + request.POST['message'])
            return render(request, self.template_name, {'message': 'با موفقیت انجام شد'})
        else:
            return redirect(reverse('users:login') + "?next=" + request.path_info)
