from django.shortcuts import render
from types import SimpleNamespace

def game(request):
    def to_dict(obj):
        return {
            'name': obj.name,
            'type': obj.type,
            'points': obj.points,
            'role': obj.prop_1,
            'pic': obj.pic
        }

    team_a = [
        SimpleNamespace(name="A Player_1", type="Player", points=100, prop_1='defend', pic='/pics/cr.jpg'),
        SimpleNamespace(name="A Player_2", type="Player", points=80, prop_1='defend', pic='/pics/standard.png'),
        SimpleNamespace(name="A Player_3", type="Player", points=120, prop_1='attack', pic='/pics/standard.png'),
        SimpleNamespace(name="A Player_4", type="Player", points=70, prop_1='middle', pic='/pics/standard.png'),
        SimpleNamespace(name="A Player_5", type="Player", points=100, prop_1='attack', pic='/pics/standard.png'),
        SimpleNamespace(name="A Player_6", type="Player", points=99, prop_1='attack', pic='/pics/standard.png'),
        SimpleNamespace(name="A Player_7", type="Player", points=110, prop_1='middle', pic='/pics/standard.png'),
    ]
    team_b = [
        SimpleNamespace(name="B Player_1", type="Player", points=95, prop_1='middle', pic='/pics/lm.jpeg'),
        SimpleNamespace(name="B Player_2", type="Player", points=85, prop_1='defend', pic='/pics/standard.png'),
        SimpleNamespace(name="B Player_3", type="Player", points=105, prop_1='attack', pic='/pics/standard.png'),
        SimpleNamespace(name="B Player_4", type="Player", points=90, prop_1='middle', pic='/pics/standard.png'),
        SimpleNamespace(name="B Player_5", type="Player", points=100, prop_1='attack', pic='/pics/standard.png'),
        SimpleNamespace(name="B Player_6", type="Player", points=98, prop_1='attack', pic='/pics/standard.png'),
        SimpleNamespace(name="B Player_7", type="Player", points=110, prop_1='middle', pic='/pics/standard.png'),
    ]

    cards = [to_dict(c) for c in team_a + team_b]

    return render(request, "game.html", {
        "cards": cards,
    })


##################################################
###################################################

from django.shortcuts import render
from game.models import Card
from players.models import Player
from django.contrib.auth.decorators import login_required
import random

@login_required
def game(request):
    def to_dict(card, team):
        return {
            'name': card.name,
            'type': card.type,
            'points': card.points,
            'role': card.prop_1,
            'pic': card.picture_url if getattr(card, 'picture_url', None) else '/pics/standard.png',
            'team': team,
        }
    try:
        player_a = Player.objects.get(user=request.user)
    except Player.DoesNotExist:
        return render(request, "game.html", {"error": "No Player profile found for current user."})

    # Get 7 cards for current user (Team A)
    all_a_cards = list(player_a.cards.all())
    team_a      = random.sample(all_a_cards, min(7, len(all_a_cards)))

    # Pick an opponent (any player that's not current user)
    opponent_player = (
        Player.objects.exclude(user=request.user)
        .order_by('user__id')
        .first()
    )
    if not opponent_player:
        return render(request, "game.html", {"error": "No opponent found."})

    all_b_cards = list(opponent_player.cards.all())
    team_b      = random.sample(all_b_cards, min(7, len(all_b_cards)))

    cards = [to_dict(card, 'A') for card in team_a] + [to_dict(card, 'B') for card in team_b]

    return render(request, "game.html", {
        "cards": cards,
        "team_a_user": request.user.username,
        "team_b_user": opponent_player.user.username,
    })




    '''
    all_a_cards = list(player_a.cards.all())
    team_a      = random.sample(all_a_cards, min(7, len(all_a_cards)))

    # Pick an opponent (any player that's not current user)
    opponent_player = (
        Player.objects.exclude(user=request.user)
        .order_by('user__id')
        .first()
    )
    if not opponent_player:
        return render(request, "game.html", {"error": "No opponent found."})

    all_b_cards = list(opponent_player.cards.all())
    team_b      = random.sample(all_b_cards, min(7, len(all_b_cards)))

    cards = [to_dict(card, 'A') for card in team_a] + [to_dict(card, 'B') for card in team_b]

    return render(request, "game.html", {
        "cards": cards,
        "team_a_user": request.user.username,
        "team_b_user": opponent_player.user.username,
    })

   '''