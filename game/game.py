def game(card, team):
    print("🔍 Processing card:", card, "Team:", team)  # Debug
    if card["type"] == "special":
        return True
    else :
        return False