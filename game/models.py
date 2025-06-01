from django.db import models
from players.models import Player


# Create your models here.

class Game(models.Model):
    match_id = models.CharField(max_length=100, unique=True)
    match_date = models.DateTimeField()
    match_type = models.CharField(max_length=50)
    player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_1')
    player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_2')
    player1_score = models.IntegerField()
    player2_score = models.IntegerField()
    winner = models.CharField(max_length=100)
    duration = models.DurationField()

class Card(models.Model):
    card_id     = models.CharField(max_length=100, unique=True)
    name        = models.CharField(max_length=100)
    type        = models.CharField(max_length=50)
    prop_1      = models.CharField(max_length=50, blank=True, null=True)
    prop_2      = models.CharField(max_length=50, blank=True, null=True)
    prop_3      = models.CharField(max_length=50, blank=True, null=True)
    points      = models.IntegerField()
    description = models.TextField()


    owners = models.ManyToManyField(Player, related_name='cards', blank=True)  # Moved here