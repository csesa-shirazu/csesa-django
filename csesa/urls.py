"""noorando URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path

from csesa import settings
# from csesa.bot_utils import bot_loop
from csesa.views import GraderyRequestAPIView, CourseGroupTAsAPIView, DestroyGraderyRequestAPIView, AcceptTAAPIView, \
  RejectTAAPIView
from . import views

urlpatterns = [
  path('', views.index_view, name='index'),
  path('graders/', views.graders_view, name='graders'),
  path('admin/', admin.site.urls),
  # path('user/', include('users.urls', namespace='users')),
  path('board/', include('telegramboard.urls', namespace='telegramboard')),
  path('qualification/', include('qualification.urls', namespace='qualification')),

  path('api/v1/user/', include('users.urls', namespace='users')),
  path('api/v1/qualification/', include('qualification.apiv1.urls', namespace='qualification-api-v1')),
  path('api/v1/graders-with-qualification/', views.GradersWithQualificationAPIView.as_view(), name='graders-with-qualification'),
  path('api/v1/course-groups/', views.CourseGroupListAPIView.as_view(), name='graders-with-qualification'),
  path('api/v1/course-group-tas/<int:pk>', CourseGroupTAsAPIView.as_view(), name='course-group-tas'),
  path('api/v1/gradery-request/<int:pk>/', GraderyRequestAPIView.as_view(), name='gradery-request'),
                                    #^ pk is from course-group
  path('api/v1/cancel-gradery-request/<int:id>/', DestroyGraderyRequestAPIView.as_view(), name='cancel-gradery-request'),
  path('api/v1/approve-gradery-request/<int:pk>/', AcceptTAAPIView.as_view(), name='approve-gradery-request'),
  path('api/v1/reject-gradery-request/<int:pk>/', RejectTAAPIView.as_view(), name='reject-gradery-request'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# bot_loop.run_as_thread()