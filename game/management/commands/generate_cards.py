from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from game.models import Card
from players.models import Player
import random
import uuid

class Command(BaseCommand):
    help = 'Generate 50 mixed test cards for User 1 and User 2 with identifiable names'

    def handle(self, *args, **kwargs):
        users = User.objects.order_by('id')[:2]
        if len(users) < 2:
            self.stderr.write("Not enough users (need at least 2).")
            return

        user1, user2 = users
        try:
            player1 = Player.objects.get(user=user1)
            player2 = Player.objects.get(user=user2)
        except Player.DoesNotExist:
            self.stderr.write("One of the users does not have a Player profile.")
            return

        def create_cards_for(player, user_prefix):
            for i in range(1, 51):
                card_type = random.choice(['player', 'special', 'trainer'])
                prop_1_choices = Card.get_allowed_prop_1_values(card_type)

                card = Card.objects.create(
                    card_id=str(uuid.uuid4()),
                    name=f"{user_prefix}_{card_type.capitalize()}{i:02d}",
                    type=card_type,
                    prop_1=random.choice(prop_1_choices),
                    prop_2=random.choice(['Optional', 'Extra', 'Power', '', None]),
                    prop_3=random.choice(['Fire', 'Water', 'Wind', '', None]),
                    points=random.randint(50, 150),
                    description=f"{user_prefix} - Test {card_type.capitalize()} Card {i:02d}"
                )
                card.owners.add(player)

        create_cards_for(player1, 'U1')
        create_cards_for(player2, 'U2')

        self.stdout.write(self.style.SUCCESS('Successfully created 50 random cards each for User 1 and User 2.'))
