from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, User
from django import forms
import json

from .fillDatabase import addAttractions
from .fillDatabase import addRestaurants
from .fillDatabase import addTravelTimes

from .testfunctions import get_itinerary
from .forms import CityForm, itinerary_form_generator, ItineraryForm

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


def choose_city(request):
    context_dict = {}
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            request.session['city'] = form_data['city']
            context_dict['city'] = form_data['city']
            return HttpResponseRedirect(reverse("ubertravel:itinerary"))


    form = CityForm()
    context_dict['form'] = form
    return render(request, "ubertravel/choose_city.html", context_dict)


def itinerary(request):
    try:
        city = request.session['city']
    # If city is not chosen redirect
    except:
        return HttpResponseRedirect(reverse("ubertravel:choose_city"))

    context_dict = {}
    if request.method == 'GET':

        events, times = get_itinerary(city, [], [])
        #form_class = itinerary_form_generator(events)
        #form = form_class()

        form = ItineraryForm(events=events)

        request.session['events'] = events
        request.session['liked_events'] = []
        request.session['disliked_events'] = []
        context_dict = {'city': city, 'form': form}
        return render(request, "ubertravel/itinerary.html", context_dict)


    elif request.method == 'POST':
        previous_events = request.session['events']
        #form_class = itinerary_form_generator(previous_events)
        #form = form_class(request.POST)

        form = ItineraryForm(request.POST, events=previous_events)

        if form.is_valid():
            form_data = form.cleaned_data

            try:
                liked_events = request.session['liked_events']
            except:
                liked_events = []

            try:
                disliked_events = request.session['disliked_events']
            except:
                disliked_events = []

            for event in previous_events:
                if form_data[event.name] == "Like":
                    liked_events.append(event)
                elif form_data[event.name] == "Dislike":
                    disliked_events.append(event)

            request.session['liked_events'] = liked_events
            request.session['disliked_events'] = disliked_events

            events, times = get_itinerary(city, excluded_attractions=disliked_events, mandatory_attractions=liked_events)
            form = ItineraryForm(events=events)
            print(form_data)

        context_dict = {'city': city, 'form': form}
        return render(request, "ubertravel/itinerary.html", context_dict)


def index_view(request):
    context_dict = {}

    addRestaurants("/home/maxi/Documents/Development/HackathonHKUST/hackust/hackust/ubertravel/CityData/Hong Kong_restaurants.json")
    addAttractions("/home/maxi/Documents/Development/HackathonHKUST/hackust/hackust/ubertravel/CityData/Hong Kong_attractions.json")
    addTravelTimes("Hong Kong")
    return render(request, 'ubertravel/index.html', context_dict)

def detail(request):
    context_dict = {}
    return render(request, 'ubertravel/detail.html', context_dict)