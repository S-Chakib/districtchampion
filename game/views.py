from django.shortcuts import render

# Create your views here.

def game(request):
    card_positions = {
    0: {"top": 20, "left": 10},
    1: {"top": 35, "left": 10},
    2: {"top": 38, "left": 8},
    3: {"top": 52, "left": 10},
    4: {"top": 55, "left": 8},
    5: {"top": 73, "left": 10},

}

    return render(request, "game.html", {
        "card_positions": card_positions,
        "card_range": range(7),
    })
