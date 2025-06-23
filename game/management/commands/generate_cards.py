from django.core.management.base import BaseCommand
from game.models import Card
from players.models import Player
import random
import uuid

class Command(BaseCommand):
    help = 'Generate 100 random Card instances and assign them to the first Player'

    def handle(self, *args, **kwargs):
        types = ['player', 'trainer', 'special']

        prop_1_map = {
            'player': Card.get_allowed_prop_1_values('player'),
            'trainer': Card.get_allowed_prop_1_values('trainer'),
            'special': Card.get_allowed_prop_1_values('special'),
        }

        # Get the first player in the DB
        try:
            owner = Player.objects.first()
            if not owner:
                self.stderr.write("❌ No Player found in database.")
                return
        except Player.DoesNotExist:
            self.stderr.write("❌ No Player found in database.")
            return

        count_per_type = 100 // len(types)
        cards = []

        for card_type in types:
            for i in range(1, count_per_type + 1):
                card_name = f"{card_type}_{i:03d}"
                card = Card(
                    card_id=str(uuid.uuid4()),
                    name=card_name,
                    type=card_type,
                    prop_1=random.choice(prop_1_map[card_type]),
                    prop_2=random.choice(['Optional', 'Extra', 'Power', '', None]),
                    prop_3=random.choice(['Fire', 'Water', 'Wind', '', None]),
                    points=random.randint(50, 150),
                    description=f"{card_type.capitalize()} card number {i:03d}"
                )
                card.save()  # Save individually to enable ManyToMany assignment
                card.owners.add(owner)

        self.stdout.write(self.style.SUCCESS('✅ Successfully created 99 cards and assigned them to the first Player.'))
