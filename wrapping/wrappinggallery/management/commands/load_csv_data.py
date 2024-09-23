import csv
import json
import os
import pandas as pd
from wrappinggallery.models import Carry, Rating
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
        if Carry.objects.exists() or Rating.objects.exists():
            self.stdout.write('Carry or Rating not empty. Clearing both.')
            Carry.objects.all().delete()
            Rating.objects.all().delete()

        dtype_dict = {
            'rings': 'bool',
            'pretied': 'bool',
            'pass_horizontal': 'int32',
            'pass_cross': 'int32',
            'pass_reinforcing_horizontal': 'int32',
            'pass_reinforcing_cross': 'int32',
            'pass_poppins': 'int32',
            'pass_ruck': 'int32',
            'pass_sling': 'int32',
            'pass_kangaroo': 'int32',
            'size': 'int32',
            'mmposition': 'int32',
            'layers': 'int32',
            'shoulders': 'int32',
            'newborns': 'int32',
            'legstraighteners': 'int32',
            'leaners': 'int32',
            'bigkids': 'int32',
            'feeding': 'int32',
            'quickups': 'int32',
            'pregnancy': 'int32',
            'fancy': 'int32',
            'difficulty': 'int32',
            'votes': 'int32',
            'other_chestpass': 'bool',
            'other_bunchedpasses': 'bool',
            'other_shoulderflip': 'bool',
            'other_twistedpass': 'bool',
            'other_eyelet': 'bool',
            'other_waistband': 'bool',
            'other_legpasses': 'bool',
            'other_s2s': 'bool',
            'other_sternum': 'bool',
            'other_poppins': 'bool',
        }

        table = pd.read_csv(csv_file, dtype=dtype_dict, encoding='latin1')
        table = table.fillna('')

        for _, row in table.iterrows():
            # Check if the Carry already exists
            if Carry.objects.filter(name=row["name"]).exists():
                self.stdout.write(self.style.WARNING(f"- Skipped {row['name']}, already exists."))
                continue

            try:
                # Create the Carry instance
                carry = Carry.objects.create(
                    name=row["name"],
                    title=row["title"],
                    longtitle=row["longtitle"],
                    size=row["size"],
                    shoulders=row["shoulders"],
                    layers=row["layers"],
                    mmposition=row["mmposition"],
                    videotutorial=row["videotutorial"],
                    videoauthor=row["videoauthor"],
                    videotutorial2=row["videotutorial2"],
                    videoauthor2=row["videoauthor2"],
                    videotutorial3=row["videotutorial3"],
                    videoauthor3=row["videoauthor3"],
                    position=row["position"],
                    description=row["description"],
                    pretied=row["pretied"],
                    rings=row["rings"],
                    pass_horizontal=row["pass_horizontal"],
                    pass_cross=row["pass_cross"],
                    pass_reinforcing_cross=row["pass_reinforcing_cross"],
                    pass_reinforcing_horizontal=row["pass_reinforcing_horizontal"],
                    pass_poppins=row["pass_poppins"],
                    pass_ruck=row["pass_ruck"],
                    pass_sling=row["pass_sling"],
                    pass_kangaroo=row["pass_kangaroo"],
                    other_chestpass=row["other_chestpass"],
                    other_bunchedpasses=row["other_bunchedpasses"],
                    other_shoulderflip=row["other_shoulderflip"],
                    other_twistedpass=row["other_twistedpass"],
                    other_waistband=row["other_waistband"],
                    other_legpasses=row["other_legpasses"],
                    other_s2s=row["other_s2s"],
                    other_eyelet=row["other_eyelet"],
                    other_poppins=row["other_poppins"],
                    other_sternum=row["other_sternum"],
                )

                # Create the Rating instance
                Rating.objects.create(
                    carry=carry,
                    newborns=row["newborns"],
                    legstraighteners=row["legstraighteners"],
                    leaners=row["leaners"],
                    bigkids=row["bigkids"],
                    feeding=row["feeding"],
                    quickups=row["quickups"],
                    pregnancy=row["pregnancy"],
                    difficulty=row["difficulty"],
                    fancy=row["fancy"],
                    votes=row["votes"],
                )

                uploaded += 1
                self.stdout.write(self.style.SUCCESS(f"- Created {row['name']}."))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating {row['name']}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully loaded {uploaded} carries to database.'))
