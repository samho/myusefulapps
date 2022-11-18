from django.shortcuts import render, redirect

# Create your views here.
from rest_framework import generics
from users.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout


from utils.dbmanager import *

# API


class UserListView(generics.ListAPIView):
    queryset = get_all_users_queryset()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveAPIView):
    queryset = get_all_users_queryset()
    serializer_class = UserSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = get_all_users_queryset()
    serializer_class = UserSerializer


class UserUpdateView(generics.UpdateAPIView):
    queryset = get_all_users_queryset()
    serializer_class = UserSerializer


class UserDeleteView(generics.DestroyAPIView):
    queryset = get_all_users_queryset()
    serializer_class = UserSerializer


class Logon(APIView):

    def post(self, request):
        result = {}
        user_list = get_user_by_name(request.data.get("username"))
        if len(user_list) == 0:
            result = {"username": "", "is_logon": False, "err_msg": "Username or Password invalid."}

        if len(user_list) >= 1:
            user = user_list[0]
            if user.is_valid(request.data.get("password")):
                result = {"username": user.username, "is_logon": True, "err_msg": None}
            else:
                result = {"username": "", "is_logon": False, "err_msg": "Username or Password invalid."}

        return Response(result)


# HTTP Request

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'users/sign-in.html')
    logon_user = request.session['logon_user']
    return render(request, 'index.html', {"logon_user": logon_user})


def userlogin(request):
    if request.method == "GET":
        return render(request, 'users/sign-in.html')
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        submit_user = authenticate(request, username=username, password=password)
        if submit_user is None:
            return render(request, 'users/sign-in.html', {"err_msg": "Username or password incorrect."})
        else:
            login(request, submit_user)
            logon_user = {"username": submit_user.first_name + ' ' + submit_user.last_name, "email": submit_user.email}
            request.session['logon_user'] = logon_user
            return render(request, 'index.html', {"logon_user": logon_user})


def userlogout(request):
    logout(request)
    request.session.delete('logon_user')
    return redirect('/')

