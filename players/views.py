from django.shortcuts import render
from game.models import Card 
from .models import Player

def user_cards(request):
    user = request.user
    cards = []
    if user.is_authenticated:
        try:
            player = Player.objects.get(user=user)
            cards = Card.objects.filter(owners=player).order_by('name')
        except Player.DoesNotExist:
            pass
    context = {
        'cards': cards,
    }
    return render(request, 'players_cards.html', context)
