from django.shortcuts               import render
from django.contrib.auth.decorators import login_required
from django.utils.timezone          import now
from datetime                       import timedelta
from game.models                    import Game
from players.models                 import Player

from .utils                         import select_cards, register_playing_cards, to_dict


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
        register_playing_cards(card_group, player, game, 'A')
    for card_group in [players_b, specials_b, trainer_b]:
        register_playing_cards(card_group, opponent_player, game, 'B')

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
    return render(request, "game.html", {
        "cards": cards,
        "team_a_user": request.user.username,
        "team_b_user": opponent_player.user.username,
        "match_id": game.match_id, 
    })


##############################################################################
