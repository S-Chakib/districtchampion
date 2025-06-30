from django.shortcuts               import render
from django.http                    import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.timezone          import now
from datetime                       import timedelta
from .models                        import Game, PlayingCard
from game.models                    import Game
from players.models                 import Player
from .utils                         import select_cards, register_playing_cards



@login_required
def start_game(request):
    player          = Player.objects.get(user=request.user)
    opponent_player = Player.objects.exclude(user=request.user).order_by('user__id').first()

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

    # Register cards for both players
    for card_group in select_cards(player):
        register_playing_cards(card_group, player, game, 'A')
    for card_group in select_cards(opponent_player):
        register_playing_cards(card_group, opponent_player, game, 'B')

    return render(request, "game.html", {
        "team_a_user": request.user.username,
        "team_b_user": opponent_player.user.username,
        "match_id": game.match_id,
    })



@login_required
def get_game_cards(match_id):
    game        = Game.objects.get(match_id=match_id)
    cardsA      = PlayingCard.objects.filter(game=game, team='A').select_related('card')
    cardsB      = PlayingCard.objects.filter(game=game, team='B').select_related('card')

    def serialize_card(pc):
        return {
            'id': pc.card.card_id,
            'name': pc.card.name,
            'type': pc.card.type,
            'points': pc.points,
            'team': pc.team,
            'p1': pc.card.prop_1,
            'pic': pc.card.picture_url or '/pics/standard.png'
        }

    return JsonResponse({
        'A': [serialize_card(card) for card in cardsA],
        'B': [serialize_card(card) for card in cardsB],
    })

##############################################################################
