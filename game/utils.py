import random
from game.models                    import PlayingCard

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

def register_playing_cards(card_list, player, game, team):
    for card in card_list:
        PlayingCard.objects.create(
            game=game,
            card=card,
            player=player,
            team=team,
            points=card.points if card.points else 0
            )