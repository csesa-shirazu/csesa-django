from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.db import transaction
from django.http import Http404

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, resolve
from django.views import View

from .forms import UserLoginForm
import imaplib


def login_view(request):
    next = request.GET.get('next')
    # title = "Login"
    title = "ورود"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect(reverse('telegram_board:send'))

    context = {}
    context["form"] = form
    context["title"] = title

    return render(request, "default_form.html", context)


def logout_view(request):
    logout(request)
    return redirect(reverse('users:login'))
