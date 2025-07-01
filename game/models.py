from django.db import models
from players.models import Player
from django.core.exceptions import ValidationError


# Create your models here.

class Game(models.Model):
    match_id        = models.CharField(max_length=100, unique=True)
    match_date      = models.DateTimeField()
    match_type      = models.CharField(max_length=50)
    player1         = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_1')
    player2         = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_2')
    player1_score   = models.IntegerField()
    player2_score   = models.IntegerField()
    winner          = models.CharField(max_length=100)
    duration        = models.DurationField()


TYPE_CHOICES            = [('player', 'Player'),('trainer', 'Trainer'),('special', 'Special')]
PLAYER_PROP_1_CHOICES   = ['Attack', 'Defense', 'Middle']
TRAINER_PROP_1_CHOICES  = ['Main', 'Assistant', 'Reserve']
SPECIAL_PROP_1_CHOICES  = ['Foul','Red Card', 'Yellow Card', 'Weather', 'Injury', 'Substitution']

class Card(models.Model):
    card_id     = models.CharField(max_length=100, unique=True)
    picture_url = models.URLField(blank=True, null=True)
    name        = models.CharField(max_length=100)
    type        = models.CharField(max_length=50, choices=TYPE_CHOICES)
    prop_1      = models.CharField(max_length=50, blank=True, null=True)
    prop_2      = models.CharField(max_length=50, blank=True, null=True)
    prop_3      = models.CharField(max_length=50, blank=True, null=True)
    points      = models.IntegerField()
    description = models.TextField()

    owners = models.ManyToManyField(Player, related_name='cards', blank=True)  

    def clean(self):
        allowed = self.get_allowed_prop_1_values(self.type)
        if self.prop_1 and self.prop_1 not in allowed:
            raise ValidationError({
                'prop_1': f"{self.type.capitalize()} cards must have prop_1 as one of: {', '.join(allowed)}"
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.type})"

    @staticmethod
    def get_allowed_prop_1_values(card_type):
        if card_type == 'player':
            return PLAYER_PROP_1_CHOICES
        elif card_type == 'trainer':
            return TRAINER_PROP_1_CHOICES
        elif card_type == 'special':
            return SPECIAL_PROP_1_CHOICES
        else:
            return []

class PlayingCard(models.Model):
    game        = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='playing_cards')
    card        = models.ForeignKey(Card, on_delete=models.CASCADE)
    player      = models.ForeignKey(Player, on_delete=models.CASCADE)
    played_at   = models.DateTimeField(auto_now_add=True)
    points      = models.IntegerField(default=0)
    team        = models.CharField(max_length=1, choices=[('A', 'Team A'), ('B', 'Team B')])
    played      = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.card.name} played by {self.player.user.username} in game {self.game.match_id}"