from django.shortcuts import render

# Create your views here.

def game(request):
    card_positions = {
    0: {"top": 20, "left": 10},
    1: {"top": 35, "left": 10},
    2: {"top": 38, "left": 8},
    4: {"top": 52, "left": 10},
    5: {"top": 55, "left": 8},
    6: {"top": 73, "left": 10},
    7: {"top": 100, "left": 100},
    8: {"top": 100, "left": 100},
    9: {"top": 100, "left": 100},
    10: {"top": 100, "left": 100},
    11: {"top": 100, "left": 100},
    12: {"top": 100, "left": 100},
    13: {"top": 100, "left": 100},
    14: {"top": 100, "left": 100},
    15: {"top": 100, "left": 100},
    16: {"top": 100, "left": 100},
    17: {"top": 100, "left": 100},
    18: {"top": 100, "left": 100},
    19: {"top": 100, "left": 100},
    20: {"top": 100, "left": 100},
    21: {"top": 100, "left": 100},
}

    return render(request, "game.html", {
        "card_positions": card_positions,
        "card_range": range(22),
    })
