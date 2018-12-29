from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View


class grader_qualification(View):
    template_name = 'grader-qualification.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = {}
            return render(request, self.template_name, context)
        else:
            return redirect(reverse('users:login') + "?next=" + request.path_info)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:

            #TODO: handle result here

            context = {}
            return render(request, self.template_name, context)
        else:
            return redirect(reverse('users:login') + "?next=" + request.path_info)

# Create your views here.
