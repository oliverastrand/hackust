from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'ubertravel'
urlpatterns = [
    path('', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login_page'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('home/', login_required(views.home), name='home'),
    path('index/', views.index_view, name='index'),
    path('choose_city/', views.choose_city, name='choose_city'),
    path('itinerary/', views.itinerary, name='itinerary'),
    path('detail/', views.detail, name='detail'),
    #path('settings/', login_required(views.settings), name='settings'),
]
