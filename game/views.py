from django.shortcuts import render
from types import SimpleNamespace

def game(request):
    def to_dict(obj):
        return {
            'name': obj.name,
            'type': obj.type,
            'points': obj.points,
            'role': obj.prop_1,
            'pic': obj.pic
        }

    team_a = [
        SimpleNamespace(name="Cristiano Ronaldo", type="Player", points=100, prop_1='Attack', pic='/pics/cr.jpg'),
        SimpleNamespace(name="BBB", type="Player", points=80, prop_1='defend', pic='/pics/standard.png'),
        SimpleNamespace(name="CCC", type="Player", points=120, prop_1='attack', pic='/pics/standard.png'),
        SimpleNamespace(name="DDD", type="Player", points=70, prop_1='middle', pic='/pics/standard.png'),
        SimpleNamespace(name="EEE", type="Player", points=100, prop_1='attack', pic='/pics/standard.png'),
        SimpleNamespace(name="FFF", type="Player", points=99, prop_1='attack', pic='/pics/standard.png'),
    ]
    team_b = [
        SimpleNamespace(name="Lionel Messi", type="Player", points=95, prop_1='middle', pic='/pics/lm.jpeg'),
        SimpleNamespace(name="YYY", type="Player", points=85, prop_1='defend', pic='/pics/standard.png'),
        SimpleNamespace(name="ZZZ", type="Player", points=105, prop_1='attack', pic='/pics/standard.png'),
        SimpleNamespace(name="WWW", type="Player", points=90, prop_1='middle', pic='/pics/standard.png'),
        SimpleNamespace(name="VVV", type="Player", points=100, prop_1='attack', pic='/pics/standard.png'),
        SimpleNamespace(name="UUU", type="Player", points=98, prop_1='attack', pic='/pics/standard.png'),
    ]

    cards = [to_dict(c) for c in team_a + team_b]

    return render(request, "game_2.html", {
        "cards": cards,
    })
