import csv
import json
import os
from wrappinggallery.models import Carry, Ratings
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError

class Command(BaseCommand):
    help = 'Load carries from CSV file to db'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The input CSV file')

    def handle(self, *args, **kwargs):
        uploaded = 0
        csv_file = kwargs['csv_file']

        # Check the file exists
        if not os.path.exists(csv_file):
            raise ValidationError(f'{csv_file} does not exist')

            # Check if the database is empty
        if Carry.objects.exists():
            raise ValidationError('Carrys is not empty.')

        if Ratings.objects.exists():
            raise ValidationError('Ratings is not empty.')

        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            data = list(reader)

            for row in data:
                # Check if the Carry already exists
                if Carry.objects.filter(name=row["name"]).exists():
                    self.stdout.write(self.style.WARNING(f"- Skipped {row['name']}, already exists."))
                    continue

                try:
                    # Create the Carry instance
                    carry = Carry.objects.create(
                        name=row["name"],
                        title=row["title"],
                        size=row["size"],
                        shoulders=row["shoulders"],
                        layers=row["layers"],
                        mmposition=row["mmposition"],
                        videotutorial=row["videotutorial"],
                        videoauthor=row["videoauthor"],
                        position=row["position"],
                        description=row["description"],
                        pretied=row["pretied"],
                        finish=row["finish"],
                    )

                    # Create the Ratings instance
                    Ratings.objects.create(
                        carry=carry,
                        newborns=row["newborns"],
                        legstraighteners=row["legstraighteners"],
                        leaners=row["leaners"],
                        bigkids=row["bigkids"],
                        feeding=row["feeding"],
                        quickups=row["quickups"],
                        difficulty=row["difficulty"],
                        fancy=row["fancy"],
                        votes=row["votes"],
                    )

                    uploaded += 1
                    self.stdout.write(self.style.SUCCESS(f"- Created {row['name']}."))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error creating {row['name']}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully loaded {uploaded} carries to database.'))
