from django.shortcuts import render
from game.models import Card
from players.models import Player
from django.contrib.auth.decorators import login_required
import random

@login_required
def game(request):
   
    player_a                            = Player.objects.get(user=request.user)
    opponent_player                     = Player.objects.exclude(user=request.user).order_by('user__id').first()
    players_a, specials_a, trainer_a    = select_cards(player_a)
    players_b, specials_b, trainer_b    = select_cards(opponent_player)
    players_a, specials_a, trainer_a    = [to_dict(card, 'A') for card in players_a], [to_dict(card, 'A') for card in specials_a], [to_dict(card, 'A') for card in trainer_a]
    players_b, specials_b, trainer_b    = [to_dict(card, 'B') for card in players_b], [to_dict(card, 'B') for card in specials_b], [to_dict(card, 'B') for card in trainer_b]

    cards = {
        'A': {'players': players_a,'specials': specials_a,'trainer': trainer_a,},
        'B': {'players': players_b,'specials': specials_b,'trainer': trainer_b,},
    }

    return render(request, "game.html", {
        "cards": cards,
        "team_a_user": request.user.username,
        "team_b_user": opponent_player.user.username,
    })


def to_dict(card, team):
    return {
        'name':     card.name,
        'type':     card.type,
        'points':   card.points,
        'role':     card.prop_1,
        'pic':      card.picture_url if getattr(card, 'picture_url', None) else '/pics/standard.png',
        'team':     team,
    }

def select_cards(player):
    cards = player.cards.all()
    print (cards)
    all_players  = list(cards.filter(type='player'))
    all_specials = list(cards.filter(type='special'))
    all_trainers = list(cards.filter(type='trainer'))

    players  = random.sample(all_players, min(7, len(all_players)))
    specials = random.sample(all_specials, min(4, len(all_specials)))
    trainers = random.sample(all_trainers, min(1, len(all_trainers)))

    return players, specials, trainers