from django.shortcuts import render
from .models import Card
from types import SimpleNamespace

from types import SimpleNamespace
from collections import defaultdict

def game(request):
    # Simulated cards
    trainer = SimpleNamespace(name="Trainer", type="Trainer", points=None, prop_1=None)

    players = [
        SimpleNamespace(name = "AAA", type = 'Player', points = 100, prop_1='middle'),
        SimpleNamespace(name = "BBB", type = 'Player', points = 80, prop_1='middle'),
        SimpleNamespace(name = "CCC", type = 'Player', points = 120, prop_1='attacking'),
        SimpleNamespace(name = "DDD", type = 'Player', points = 70, prop_1='middle'),
        SimpleNamespace(name = "EEE", type = 'Player', points = 100, prop_1='defining'),
        SimpleNamespace(name = "FFF", type = 'Player', points = 99, prop_1='attacking'),
    ]

    left_map = {
        'defining': 21,
        'middle': 30,
        'attacking': 40
    }

    base_top = 30
    vertical_spacing = 20  # Adjust this to control vertical space between stacked cards

    # Group by left positions
    grouped_by_left = defaultdict(list)
    for i, card in enumerate(players, start=1):
        left = left_map.get(card.prop_1, 10)
        grouped_by_left[left].append(i)

    card_positions = {0: {"top": 20, "left": 10}}  # Trainer card

    # Assign top/left values, stacking vertically within each group
    for left, indices in grouped_by_left.items():
        for j, card_index in enumerate(indices):
            top = base_top + j * vertical_spacing
            card_positions[card_index] = {"top": top, "left": left}

    cards =  [trainer] + players

    return render(request, "game.html", {
    "card_positions": card_positions,
    "card_range": range(1, 7),  # Show only player cards (1 to 6)
    "cards": cards,
    
})








    '''
    card_positions = {
    0: {"top": 20, "left": 10},
    1: {"top": 35, "left": 10},
    2: {"top": 38, "left": 8},
    3: {"top": 52, "left": 10},
    4: {"top": 55, "left": 8},
    5: {"top": 73, "left": 10},

    }
    '''
    