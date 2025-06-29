

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    path('game/', views.start_game, name='start_game'),
    path("game/play_card/", views.play_card, name="play_card"),

]
