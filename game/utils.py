import random
from game.models                    import PlayingCard


def select_cards(player):
    cards = player.cards.all()
    all_players  = list(cards.filter(type='player'))
    all_specials = list(cards.filter(type='special'))
    all_trainers = list(cards.filter(type='trainer'))

    players  = random.sample(all_players, min(7, len(all_players)))
    specials = random.sample(all_specials, min(4, len(all_specials)))
    trainers = random.sample(all_trainers, min(1, len(all_trainers)))

    return players, specials, trainers

def register_playing_cards(card_list, player, game, team):
    cards = []
    for card in card_list:
        playingCard = PlayingCard.objects.create(
            game=game,
            card=card,
            player=player,
            team=team,
            points=card.points if card.points else 0
            )
        cards.append(playingCard)
    return cards