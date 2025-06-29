from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json

@csrf_exempt  
@require_POST
@login_required
def play_card(request):
    try:
        data = json.loads(request.body)
        card = data.get("card")
        target = data.get("target")  # Optional

        if not card:
            return JsonResponse({"error": "Missing card"}, status=400)

        # Load current state
        game_state = request.session.get("game_state")
        if not game_state:
            return JsonResponse({"error": "No game state"}, status=400)

        cards = game_state["cards"]
        team = card["team"]
        prop = card.get("prop_1", "").lower()

        # ✅ Foul Rule: Remove 1 point from selected target
        if prop == "foul" and target:
            opponent_team = "B" if team == "A" else "A"
            for c in cards[opponent_team]["players"]:
                if c["name"] == target["name"]:
                    c["points"] = max(0, c["points"] - 1)
                    print(f"Foul applied to {c['name']} → {c['points']} pts")
                    break

        # Save back
        request.session["game_state"]["cards"] = cards
        request.session.modified = True
        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
