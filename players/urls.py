from django.urls import path
from . import views

app_name = 'players'

urlpatterns = [
    
    path('', views.user_cards, name='user_cards'),
]