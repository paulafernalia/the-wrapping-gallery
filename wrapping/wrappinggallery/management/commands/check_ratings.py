from django.core.management.base import BaseCommand

from wrappinggallery.models import Carry, Rating


class Command(BaseCommand):
    help = "Check that every Carry has a corresponding Rating"

    def handle(self, *args, **kwargs):
        all_carries = Carry.objects.all()
        carries_without_ratings = [
            carry
            for carry in all_carries
            if not Rating.objects.filter(carry=carry).exists()
        ]

        if carries_without_ratings:
            missing_carries = ", ".join(
                str(carry.name) for carry in carries_without_ratings
            )
            self.stdout.write(
                self.style.ERROR(
                    f"The following Carry IDs do not have corresponding Rating: {missing_carries}"
                )
            )
            self.stdout.write(
                self.style.ERROR(
                    f"Total missing ratings: {len(carries_without_ratings)}"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "All Carry entries have corresponding Rating entries."
                )
            )
