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
    context = {}
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
    elif request.POST: # Data is submitted and invalid
            context['error'] = True
    if request.user.is_authenticated:
        if next:
            return redirect(next)
        return redirect(reverse('qualification:form', kwargs={'slug': 'cse-gradery'}))

    return render(request, "login.html", context)


def logout_view(request):
    logout(request)
    return redirect(reverse('users:login'))
