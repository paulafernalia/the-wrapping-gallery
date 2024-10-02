from django.dispatch import receiver
from .models import Carry, UserRating, CustomUser, DoneCarry
from django.db.models.signals import pre_delete, post_delete, post_save
from .achievements import ACHIEVEMENT_FUNCTIONS
from .models import UserAchievement, Achievement


def recalculate_achievements(user, type):
    print(f"recalculate {type} achievements")
    
    # Get support data based on the type
    if type == "done_carries":
        support_data = DoneCarry.objects.filter(user=user)
    elif type == "ratings":
        support_data = UserRating.objects.filter(user=user)
    elif type == "user":
        support_data = user
    elif type == "general_ratings":
        user_done_carries = DoneCarry.objects.filter(user=user)
        carry_names = support_data.values_list('carry__name', flat=True)
        support_data = Rating.objects.filter(carry__name__in=carry_names)
    else:
        raise ValidationError(f"Unknown type {type}")
    
    # Retrieve all necessary achievements and user achievements in bulk
    achievements = Achievement.objects.filter(name__in=ACHIEVEMENT_FUNCTIONS.keys())
    achievements_dict = {achievement.name: achievement for achievement in achievements}
    
    user_achievements = UserAchievement.objects.filter(user=user)
    user_achievements_dict = {ua.achievement.name: ua for ua in user_achievements}        
    
    for achievement_name, (func, data_type, kwargs) in ACHIEVEMENT_FUNCTIONS.items():
        if achievement_name in achievements_dict:
            achievement = achievements_dict[achievement_name]
            
            # Check if this function applies to the current type
            if data_type == type:
                if func(support_data, **kwargs):  # Pass the done carries or ratings
                    if achievement_name not in user_achievements_dict:
                        UserAchievement.objects.create(achievement=achievement, user=user)
                else:
                    if achievement_name in user_achievements_dict:
                        user_achievements_dict[achievement_name].delete()


# Recalculate achievements after DoneCarry is created/updated.
@receiver(post_save, sender=DoneCarry, weak=True)
def handle_save(sender, instance, **kwargs):
    recalculate_achievements(instance.user, "done_carries")

# Recalculate achievements after UserRating is created/updated.
@receiver(post_save, sender=UserRating, weak=True)
def handle_save(sender, instance, **kwargs):
    recalculate_achievements(instance.user, "ratings")

# Recalculate achievements after DoneCarry is deleted.
@receiver(post_delete, sender=DoneCarry, weak=True)
def handle_delete(sender, instance, **kwargs):
    recalculate_achievements(instance.user, "done_carries")

# Recalculate achievements after UserRating is deleted.
@receiver(post_delete, sender=UserRating, weak=True)
def handle_delete(sender, instance, **kwargs):
    recalculate_achievements(instance.user, "ratings")

# Recalculate achievements after a new Achievement is created/updated.
@receiver(post_save, sender=Achievement, weak=True)
def handle_achievement_save(sender, instance, created, **kwargs):
    # If a new achievement is created, recalculate for all users
    users = CustomUser.objects.all()  # Adjust this if you have a different user model
    for user in users:
        recalculate_achievements(user, "ratings")
        recalculate_achievements(user, "done_carries")
        recalculate_achievements(user, "user")
