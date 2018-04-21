from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, User
from django import forms
import json


# Imports for registering users from

from django.core.mail import send_mail



def login_user(request):
    #question = get_object_or_404(Question, pk=question_id)

    username = request.POST["username"]
    password = request.POST["password"]
    next_page = request.POST["next"]

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        if next_page:
            return HttpResponseRedirect(next_page)
        else:
            return HttpResponseRedirect(reverse("ubertravel:home"))
    else:
        #return HttpResponseRedirect(reverse("polls:login_page"))
        return render(request, "registration/login.html", {
            'error_message': "Could not find user",
        })

def home(request):
    return render(request, "ubertravel/home.html")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("ubertravel:login_page"))