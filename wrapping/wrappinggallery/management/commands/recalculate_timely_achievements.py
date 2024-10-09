from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from wrappinggallery.models import recalculate_achievements

User = get_user_model()

class Command(BaseCommand):
    help = 'Recalculates timely achievements for all users'

    def handle(self, *args, **kwargs):
        # Get all users
        users = User.objects.all()

        # Loop through all users and recalculate their achievements
        for user in users:
            # Call recalculate_achievements function for both 'done_carries' and 'ratings'
            recalculate_achievements(user, "time")

        self.stdout.write(self.style.SUCCESS(
            'Successfully recalculated user achievements for all users'))
