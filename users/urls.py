from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = 'users'
urlpatterns = [
    # path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),  # <-- And here
]