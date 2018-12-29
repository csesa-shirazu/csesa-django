from django.shortcuts import render, redirect
from django.urls import reverse


def index_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('qualification:cse_gradery'))
    else:
        return redirect(reverse('users:login') + "?next=" + reverse('qualification:cse_gradery'))

