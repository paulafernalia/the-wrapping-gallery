from django.dispatch import receiver
from .models import Carry, UserRating, CustomUser
from django.db.models.signals import pre_delete

@receiver(pre_delete, sender=CustomUser)
def user_rating_cleanup(sender, instance, **kwargs):
    user_ratings = UserRating.objects.filter(user=instance)
    for user_rating in user_ratings:
        user_rating.delete()  # This will call the delete method you defined
