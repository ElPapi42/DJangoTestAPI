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
        status = 200
        response = []

        user_data = request.POST
        
        if(not request.user.is_authenticated):
            if(not User.objects.filter(username=user_data["username"]).exists()):

                user = User.objects.create_user(user_data["username"], user_data["email"], user_data["password"])
                user.save()

                response.append({
                    "Status":"Success Register [Code {status}]".format(status=status), 
                    "Username":user.username, 
                    "eMail":user.email
                })
            else:
                status = 406
                response.append({
                    "Status":"Failure Register [Code {status}]".format(status=status), 
                    "Reason":"User already registered"
                })
        else:
            status = 400
            response.append({
                "Status":"Failure Register [Code {status}]".format(status=status),  
                "Reason":"Attemp to register new user from logged session"
            })

        return JsonResponse(response, safe=False, status=status)

class Login(View):
    """Login an user to the session"""

    def post(self, request, *args, **kwargs):
        status = 200
        response = []

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request=request, username=username, password=password)

        if(user):

            login(request, user)

            response.append({
                "Status":"Success Login [Code {status}]".format(status=status), 
                "Username":user.username, 
                "eMail":user.email
            })
        else:
            status = 404
            response.append({
                "Status":"Failure Login [Code {status}]".format(status=status), 
                "Reason":"Submitted data invalid, check again"
            })

        return JsonResponse(response, safe=False, status=status)

class Logout(View):
    "Logout the user, if thereis one user loged in"

    def post(self, request, *args, **kwargs):
        status = 200
        response = []

        if(request.user.is_authenticated):
            user = User.objects.get(id=request.user.id)   
            logout(request)
            
            response.append({
                "Status":"Success Logout [Code {status}]".format(status=status), 
                "Username":user.username, 
                "eMail":user.email
            })
        else:
            status = 401
            response.append({
                "Status":"Failure Logout [Code {status}]".format(status=status), 
                "Reason":"You must Login for be able to Logout"
            })

        return JsonResponse(response, safe=False, status=status)

class LoggedUserProfile(View):
    """Return details of the user logged currently in the session"""

    def get(self, request, username=None, *args, **kwargs):
        status = 200
        response = []

        if(request.user.is_authenticated):
            user = request.user

            response.append({
                "Status":"Success UserRetreived [Code {status}]".format(status=status), 
                "Username":user.username, 
                "eMail":user.email
            })
        else:
            status = 401
            response.append({
                "Status":"Failure [Code {status}]".format(status=status), 
                "Reason":"You must be logged in for see this content"
            })

        return JsonResponse(response, safe=False, status=status)

class UserProfile(View):
    """Return details of public profile of an user"""

    def get(self, request, username=None, *args, **kwargs):
        status = 200
        response = []

        if(request.user.is_authenticated):

            if(User.objects.filter(username=username).exists()):

                user = User.objects.get_by_natural_key(username=username)

                if(user == request.user):
                    response = redirect("rest_api:user_me")
                    return response
                else:
                    response.append({
                        "Status":"Success UserRetreived [Code {status}]".format(status=status), 
                        "Username":user.username, 
                        "eMail":user.email
                    })
            else:
                status = 404
                response.append({
                    "Status":"Failure [Code {status}]".format(status=status), 
                    "Reason":"Requested user not found"
                })
        else:
            status = 401
            response.append({
                "Status":"Failure [Code {status}]".format(status=status), 
                "Reason":"You must be logged in for see this content"
            })
        
        return JsonResponse(response, safe=False, status=status)

