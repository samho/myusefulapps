from django.urls import path
from users import views
app_name = 'users'

urlpatterns = [
    path('users/delete/<pk>/',
         views.UserDeleteView.as_view(),
         name='user_delete'),
    path('users/update/<pk>/',
         views.UserUpdateView.as_view(),
         name='user_update'),
    path('users/create/',
         views.UserCreateView.as_view(),
         name='user_create'),
    path('users/logon/',
         views.Logon.as_view(),
         name='user_logon'),
    path('users/',
         views.UserListView.as_view(),
         name='users_list'),
    path('users/<pk>/',
         views.UserDetailView.as_view(),
         name='user_detail'),
]
