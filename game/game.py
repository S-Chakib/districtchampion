def game(card_id, target_players=[]):
    from .models import PlayingCard
    try:
       
        card        = PlayingCard.objects.get(pk=card_id)
        card.played = True
        card.save()

        target_players = [int(player_id) for player_id in target_players]
        for player_id in target_players:
            try:
                player_card = PlayingCard.objects.get(pk=player_id, game=card.game)
                print (player_card.card.name, player_card.points)
                player_card.points = player_card.points - card.points
                if player_card.points < 0:
                    player_card.points = 0
                player_card.save()
                print(f"✅ Updated points for card {player_card.id}: {player_card.points}")
            except PlayingCard.DoesNotExist:
                print(f"❌ Player Card with id {player_id} does not exist in this game.")
        '''
        
        
        
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
        '''

    except PlayingCard.DoesNotExist:
        print(f"PlayingCard with id {card_id} does not exist!")
        return False

    except Exception as e:
        print(f"Unexpected error occurred: {str(e)}")
        return False