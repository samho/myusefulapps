"""myusefulapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from users.views import index, userlogin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sampleapi/', include('sample.api.urls', namespace='api')),
    path('api/token/', obtain_auth_token, name='api-token'),
    path('api/usersapi/', include('users.api.urls', namespace='userapi')),
    path('users/', include('users.urls', namespace='users')),
    path('commontype/', include('commontype.urls', namespace='commontype')),
    path('', userlogin, name='user_login'),
    path('index/', index, name='index'),
]
