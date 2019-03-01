from django.contrib import admin
from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, ContactView, Logout, PostUpdateView, PostDeleteView
from django.contrib.auth import views as auth_views

app_name = 'telegramboard'
urlpatterns = [
    path('', PostListView.as_view(), name='telegramboard-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('login/', auth_views.LoginView.as_view(template_name='telegramboard/login.html'), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('contact/', ContactView, name='contact'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),

]
