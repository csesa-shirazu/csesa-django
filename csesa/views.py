from django.shortcuts import render, redirect
from django.urls import reverse


def index_view(request):
    return render(request, "index.html", {})

