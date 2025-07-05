def game(card_id):
    from .models import PlayingCard
    try:
       
        card = PlayingCard.objects.get(pk=card_id)

        card.played = True
        card.save()

        if card.card.type == "special":
            player_cards = PlayingCard.objects.filter(game=card.game, card__type="player")
            
            for player_card in player_cards:
                old_points = player_card.points
                player_card.points -= 10
                player_card.save()
                print(f"✅ Updated points for card {player_card.id}: {old_points} -> {player_card.points}")
            return True
        else:
            print("Player Card played") 
            return False

    except PlayingCard.DoesNotExist:
        print(f"PlayingCard with id {card_id} does not exist!")
        return False

    except Exception as e:
        print(f"Unexpected error occurred: {str(e)}")
        return False