import random
from asgiref.sync                   import async_to_sync
from channels.layers                import get_channel_layer
from django.shortcuts               import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone          import now
from django.http                    import JsonResponse
from datetime                       import timedelta
from .sp_cards_rules                import play_card 
from game.models                    import Game, PlayingCard
from players.models                 import Player


@login_required
def start_game(request):
   
    player                              = Player.objects.get(user=request.user)
    opponent_player                     = Player.objects.exclude(user=request.user).order_by('user__id').first()
    
    game = Game.objects.create(
        match_id        = f"{player.user.username}_vs_{opponent_player.user.username}_{now().strftime('%Y%m%d%H%M%S')}",
        match_date      = now(),
        match_type      = "Standard",
        player1         = player,
        player2         = opponent_player,
        player1_score   = 0,
        player2_score   = 0,
        winner          = '',
        duration        = timedelta(),
    )
    
    # Select the cards for both from their playing cards.
    players_a, specials_a, trainer_a    = select_cards(player)
    players_b, specials_b, trainer_b    = select_cards(opponent_player)

    # Register the selected cards as playing cards in the game.
    # This will create PlayingCard instances for each selected card.
    for card_group in [players_a, specials_a, trainer_a]:
        register_playing_cards(card_group, player, game)
    for card_group in [players_b, specials_b, trainer_b]:
        register_playing_cards(card_group, opponent_player, game)

    # Convert the selected cards to dictionaries for rendering in the template.
    # This is necessary to pass the data to the frontend.
    players_a_dict  = [to_dict(card, 'A') for card in players_a]
    specials_a_dict = [to_dict(card, 'A') for card in specials_a]
    trainer_a_dict  = [to_dict(card, 'A') for card in trainer_a]
    players_b_dict  = [to_dict(card, 'B') for card in players_b]
    specials_b_dict = [to_dict(card, 'B') for card in specials_b]
    trainer_b_dict  = [to_dict(card, 'B') for card in trainer_b]

    cards = {
        'A': {'players': players_a_dict, 'specials': specials_a_dict, 'trainer': trainer_a_dict},
        'B': {'players': players_b_dict, 'specials': specials_b_dict, 'trainer': trainer_b_dict},
    }
    print(game.match_id)
    return render(request, "game.html", {
        "cards": cards,
        "team_a_user": request.user.username,
        "team_b_user": opponent_player.user.username,
        "match_id": game.match_id,  # Optional: return match ID for AJAX later
    })

@login_required
def game(request):
    match_id        = request.POST.get("match_id")
    card_id         = request.POST.get("card_id")
    target_card_id  = request.POST.get("target_card_id")

    game            = get_object_or_404(Game, match_id=match_id)
    player          = get_object_or_404(Player, user=request.user)

    try:
        playing_card = PlayingCard.objects.get(game=game, card_id=card_id, player=player)
    except PlayingCard.DoesNotExist:
        return JsonResponse({"error": "Card not found or not owned by you in this game"}, status=403)


    playing_card.played_at = now()
    playing_card.save()


    result = play_card(game=game, card=playing_card, target_card_id=target_card_id)

    # 🔄 Send WebSocket update
    

    channel_layer   = get_channel_layer()
    group_name      = f"game_{game.match_id}"

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "game.message",
            "message": f"{playing_card.card.name} played by {player.user.username}",
            "card": {
                "name": playing_card.card.name,
                "points": playing_card.card.points,
                "p1": playing_card.card.prop_1,
                "type": playing_card.card.type,
                "pic": playing_card.card.picture_url if playing_card.card.picture_url else "/pics/standard.png",
                "team": "A" if player == game.player1 else "B",
            },
            "team": "A" if player == game.player1 else "B",
        }
    )

    return JsonResponse({
        "message": "Card played",
        "played_card": playing_card.card.name,
        "new_state": result
    })

##############################################################################
def to_dict(card, team):
    return {
        'name':     card.name,
        'type':     card.type,
        'points':   card.points,
        'p1':       card.prop_1,
        'pic':      card.picture_url if getattr(card, 'picture_url', None) else '/pics/standard.png',
        'team':     team,
    }

def select_cards(player):
    cards = player.cards.all()
    all_players  = list(cards.filter(type='player'))
    all_specials = list(cards.filter(type='special'))
    all_trainers = list(cards.filter(type='trainer'))

    players  = random.sample(all_players, min(7, len(all_players)))
    specials = random.sample(all_specials, min(4, len(all_specials)))
    trainers = random.sample(all_trainers, min(1, len(all_trainers)))

    return players, specials, trainers

def register_playing_cards(card_list, player, game):
    for card in card_list:
        PlayingCard.objects.create(
            game=game,
            card=card,
            player=player,
            )