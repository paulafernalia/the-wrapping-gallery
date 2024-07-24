from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Carry, Ratings

@receiver(post_save, sender=Carry)
def create_ratings_for_carry(sender, instance, created, **kwargs):
    if created:  # Check if the Carry instance was created
        Ratings.objects.get_or_create(carry=instance)
