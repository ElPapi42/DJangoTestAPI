from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

import pdb

class Register(View):
    """Register New User to the Database"""

    def post(self, request, *args, **kwargs):
        user_data = request.POST
        if(not request.user.is_authenticated):
            if(not User.objects.filter(username=user_data["username"]).exists()):
                user_ref = User.objects.create_user(user_data["username"], user_data["email"], user_data["password"])
                user_ref.save()
                return HttpResponse("Registered: " + user_ref.username + " -> " + user_ref.email)
            else:
                return HttpResponse("User already registered")
        else:
            return HttpResponse("Logout before register a new account")

class Login(View):
    """Login an user to the session"""

    def post(self, request, *args, **kwargs):
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request=request, username=username, password=password)

        if(user):
            login(request, user)
            return HttpResponse("Loged In: " + user.username + " -> " + user.email)
        else:
            return HttpResponse("Invalid Credentials")

class Logout(View):
    "Logout the user, if thereis one user loged in"

    def post(self, request, *args, **kwargs):
        if(request.user.is_authenticated):
            username = User.objects.get(id=request.user.id).username   
            logout(request)
            return HttpResponse("Loged Out " + username)
        else:
            return HttpResponse("There is not logged user") 

class LoggedUserProfile(View):
    """Return details of the user logged currently in the session"""

    def get(self, request, username=None, *args, **kwargs):
        if(request.user.is_authenticated):
            user = request.user
            return HttpResponse(
                        "User Name: " + user.username + "\n" +
                        "eMail: " + user.email
                    )
        else:
            return HttpResponse("You must be logged in for see this content")

class UserProfile(View):
    """Return details of public profile of an user"""

    def get(self, request, username=None, *args, **kwargs):
        if(request.user.is_authenticated):

            if(User.objects.filter(username=username).exists()):

                user = User.objects.get_by_natural_key(username=username)

                if(user == request.user):
                    response = redirect("rest_api:user_me")
                    return response
                else:
                    return HttpResponse(
                        "User Name: " + user.username + "\n" +
                        "eMail: " + user.email
                    )
            else:
                return HttpResponse("Requested user not found")
        else:
            return HttpResponse("You must be logged in for see this content")

