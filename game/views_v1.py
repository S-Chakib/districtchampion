from django.shortcuts import render
from types import SimpleNamespace

def game(request):
    # Team A (your team)
    team_a = [
        SimpleNamespace(name="Trainer A", type="Trainer", points=None, prop_1='trainer'),
        SimpleNamespace(name="AAA", type="Player", points=100, prop_1='middle'),
        SimpleNamespace(name="BBB", type="Player", points=80, prop_1='defend'),
        SimpleNamespace(name="CCC", type="Player", points=120, prop_1='attack'),
        SimpleNamespace(name="DDD", type="Player", points=70, prop_1='middle'),
        SimpleNamespace(name="EEE", type="Player", points=100, prop_1='attack'),
        SimpleNamespace(name="FFF", type="Player", points=99, prop_1='attack'),
    ]

    left_map_a = {
        'trainer': 10,
        'defend': 21,
        'middle': 30,
        'attack': 39,
    }

    # Team B (adversary team)
    team_b = [
        SimpleNamespace(name="Trainer B", type="Trainer", points=None, prop_1='trainer'),
        SimpleNamespace(name="XXX", type="Player", points=95, prop_1='middle'),
        SimpleNamespace(name="YYY", type="Player", points=85, prop_1='defend'),
        SimpleNamespace(name="ZZZ", type="Player", points=105, prop_1='attack'),
        SimpleNamespace(name="WWW", type="Player", points=90, prop_1='middle'),
        SimpleNamespace(name="VVV", type="Player", points=100, prop_1='attack'),
        SimpleNamespace(name="UUU", type="Player", points=98, prop_1='attack'),
    ]

    left_map_b = {
        'trainer': 83,
        'defend': 73,
        'middle': 63,
        'attack': 54,
    }

    # Team A (bottom team)
    positions_a = compute_card_positions(
        team_a,
        left_map_a,
        trainer_top=10,         # Trainer A near the top
        player_base_top=27      # Players A stacked below trainer
    )

    # Team B (top team)
    positions_b = compute_card_positions(
        team_b,
        left_map_b,
        trainer_top=80,         # Trainer B near bottom
        player_base_top=20      # Players B stacked above trainer
    )
    
    # Offset team B index to avoid overlap in template (7+)
    offset = len(team_a)
    cards = team_a + team_b
    card_positions = {}

    for k, v in positions_a.items():
        card_positions[k] = v

    for k, v in positions_b.items():
        card_positions[k + offset] = v  # shift B's indices

    return render(request, "game_2.html", {
        "cards": cards,
        "card_positions": card_positions,
    })

from collections import defaultdict

def compute_card_positions(team, left_map, trainer_top=10, player_base_top=30):
    """
    Computes positions for a team with separate heights for trainer and players.
    """
    card_positions = {}

    # 1. Trainer (always index 0)
    card_positions[0] = {
        "top": trainer_top,
        "left": left_map.get(team[0].prop_1, 10)
    }

    # 2. Players (from index 1 on)
    vertical_spacing = 20
    grouped_by_left = defaultdict(list)

    for i, player in enumerate(team[1:], start=1):
        left = left_map.get(player.prop_1, 10)
        grouped_by_left[left].append(i)

    for left, indices in grouped_by_left.items():
        for j, idx in enumerate(indices):
            top = player_base_top + j * vertical_spacing
            card_positions[idx] = {"top": top, "left": left}

    return card_positions
