from django.urls import path
from users import views
app_name = 'users'

urlpatterns = [
    path('', views.index, name='user_index'),
    path('login/', views.userlogin, name='user_login'),
    path('logout/', views.userlogout, name='user_logout'),
]
