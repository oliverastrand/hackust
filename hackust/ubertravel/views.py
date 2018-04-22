from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from .testfunctions import get_itinerary
from .forms import CityForm

def login_user(request):

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

    if request.method == 'GET':

        events, times = get_itinerary(city, [], [])
        uber_times = [15, 20, 25, 20, 15, 20]
        for i in range(len(events)):
            events[i].time = times[i]
            events[i].uber_time = uber_times[i]

        request.session['events'] = events
        request.session['liked_events'] = []
        request.session['disliked_events'] = []
        request.session["times"] = times

        return render(request, "ubertravel/itinerary.html", {"events": events, "times": times, "city": city})


    elif request.method == 'POST':
        request.session["curr_event_index"] = 0

        return HttpResponseRedirect(reverse("ubertravel:detail"))

def index_view(request):
    context_dict = {}
    return render(request, 'ubertravel/index.html', context_dict)

# Returns an event object with a given name from session
def get_event(request):
    curr_event_index = request.session["curr_event_index"]
    all_events = request.session['events']
    return all_events[curr_event_index]

def next_event(request):
    request.session["curr_event_index"] += 1
    return HttpResponseRedirect(reverse("ubertravel:detail"))

def prev_event(request):
    curr_index = request.session["curr_event_index"]
    if curr_index > 0:
        request.session["curr_event_index"] -= 1
    return HttpResponseRedirect(reverse("ubertravel:detail"))

def detail(request):
    event = get_event(request)
    return render(request, 'ubertravel/detail.html', {"event": event})