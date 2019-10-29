from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json

import pdb

class Register(View):
    """Register New User to the Database"""

    def post(self, request, *args, **kwargs):

        user_data = request.POST

        #No user must be logged in while regitering new account
        if(request.user.is_authenticated):
            return JsonResponse({
                "status": "unauthorized",
                "data": "Cant register while Logged in"
            }, safe=False, status=401)

        #If user data is already on DB, avoid registration
        if(User.objects.filter(username=user_data["username"]).exists()):
            return JsonResponse({
                "status": "not acceptable",
                "data": "User already registered"
            }, safe=False, status=406)

        #Add new user to DB
        user = User.objects.create_user(user_data["username"], user_data["email"], user_data["password"])
        user.save()

        #Return new user data
        return JsonResponse({
            "status": "ok",
            "data": {
                "username":user.username,
                "email":user.email
            },
        }, safe=False, status=200)

class Login(View):
    """Login an user to the session"""

    def post(self, request, *args, **kwargs):

        #Extract username and password from request
        username = request.POST["username"]
        password = request.POST["password"]

        #Check if user credentials are valid
        auth_user = authenticate(request=request, username=username, password=password)
        if(not auth_user):
            return JsonResponse({
                "status": "unauthorized",
                "data": "Invalid credentials"
            }, safe=False, status=404)

        #Open session with the user
        login(request, auth_user)

        #Return new user data
        return JsonResponse({
            "status": "ok",
            "data": {
                "username":auth_user.username,
                "email":auth_user.email
            },
        }, safe=False, status=200)

class Logout(View):
    "Logout the user, if thereis one user loged in"

    def post(self, request, *args, **kwargs):

        #Check if the user is not auth
        if(not request.user.is_authenticated):
            return JsonResponse({
                "status": "unauthorized",
                "data": "Require login"
            }, safe=False, status=401)

        user = User.objects.get(id=request.user.id)   
        logout(request)

        #Return new user data
        return JsonResponse({
            "status": "ok",
            "data": {
                "username":user.username,
                "email":user.email
            },
        }, safe=False, status=200)

class UserProfile(View):
    """Return details of public profile of an user"""

    def get(self, request, username=None, *args, **kwargs):

        #Check if the user is not auth
        if(not request.user.is_authenticated):
            return JsonResponse({
                "status": "unauthorized",
                "data": "Login for access"
            }, safe=False, status=401)

        #Check is requested user exists
        if(not User.objects.filter(username=username).exists()):
            return JsonResponse({
                "status": "not found",
                "data": "User not found"
            }, safe=False, status=404)

        #Get reference
        user = User.objects.get_by_natural_key(username=username)

        #Return requested user data
        return JsonResponse({
            "status": "ok",
            "data": {
                "username":user.username,
                "email":user.email
            },
        }, safe=False, status=200)
