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
        
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        
            for row in data:
                # Check that this carry doesn't already exist, if so, skip
                result = Carry.objects.filter(name=row["name"])

                if result.count() == 0:
                    carry = Carry.objects.update_or_create(
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

                    ratings = Ratings.objects.update_or_create(
                        carry=carry,
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
                    carry.save()
                    ratings.save()

                    print(f"- Created {row["name"]}.")
                else:
                    carry = result[0]

                    update = input(f"Do you want to update {row['name']}? ([y]/n): ").strip().lower()
                    if update in ["y", ""]:
                        carry.title = row["title"]
                        carry.size = row["size"]
                        carry.shoulders = row["shoulders"]
                        carry.layers = row["layers"]
                        carry.mmposition = row["mmposition"]
                        carry.videotutorial = row["videotutorial"]
                        carry.videoauthor = row["videoauthor"]
                        carry.position = row["position"]
                        carry.description = row["description"]
                        carry.pretied = row["pretied"]
                        carry.finish = row["finish"]

                        ratings = Ratings.objects.get(carry__name=row["name"])
                        ratings.legstraighteners = row["legstraighteners"]
                        ratings.leaners = row["leaners"]
                        ratings.bigkids = row["bigkids"]
                        ratings.feeding = row["feeding"]
                        ratings.quickups = row["quickups"]
                        ratings.difficulty = row["difficulty"]
                        ratings.fancy = row["fancy"]
                        ratings.votes = row["votes"]

                        uploaded += 1
                        carry.save()
                        ratings.save()

                        self.stdout.write(self.style.SUCCESS(f"- Updated {row['name']}."))
                    else:
                        self.stdout.write(self.style.NOTICE(f"- Skipped updating {row['name']}."))
        
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully loaded or updated {uploaded} carries to database.'))
