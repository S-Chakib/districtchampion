

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    path('game/', views.start_game, name='start_game'),
    path('<str:match_id>/cards/', views.get_game_cards, name='get_game_cards'),

]
