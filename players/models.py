from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

class Player(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    points          = models.IntegerField(default=0)
    level           = models.IntegerField(default=1)
    rank            = models.CharField(max_length=10, default='Bronze')
    matches_played  = models.IntegerField(default=0)
    matches_won     = models.IntegerField(default=0)
    likes           = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.user.username}'s Profile"
    

@receiver(post_save, sender=User)
def create_player_profile(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_player_profile(sender, instance, **kwargs):
    if hasattr(instance, 'player'):
        instance.player.save()

