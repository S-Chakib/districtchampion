def game(card_id):
    from .models import PlayingCard
    try:
       
        card = PlayingCard.objects.get(pk=card_id)

        card.played = True
        card.save()

        if card.card.type == "special":
            print(f"🔍 Card type is 'special', reducing points for all 'player' cards in the game.")  # Debugging line

            player_cards = PlayingCard.objects.filter(game=card.game, card__type="player")
            print(f"✅ Found {player_cards.count()} 'player' cards to update.")  # Debugging line

            for player_card in player_cards:
                old_points = player_card.points
                player_card.points -= 10
                player_card.save()
                print(f"✅ Updated points for card {player_card.id}: {old_points} -> {player_card.points}")  # Debugging line

            print("✅ Successfully reduced points for all 'player' cards.")
            return True
        else:
            print(f"ℹ️ Card type is not 'special'. No points reduction applied.")  # Debugging line
            return False

    except PlayingCard.DoesNotExist:
        print(f"❌ PlayingCard with id {card_id} does not exist!")
        return False

    except Exception as e:
        print(f"❌ Unexpected error occurred: {str(e)}")
        return False