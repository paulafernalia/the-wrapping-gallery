import csv
import json
import os
import pandas as pd
from wrappinggallery.models import Carry, Rating, UserRating, CustomUser
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    help = 'Load carries from CSV file to db'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The input CSV file')


    def read_carry_csv(self, filepath):
        # Check the file exists
        if not os.path.exists(filepath):
            raise ValidationError(f'{filepath} does not exist')

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

        table = pd.read_csv(filepath, dtype=dtype_dict, encoding='latin1')
        table = table.fillna('')

        return table

    def delete_carries_not_in_file(self, df):
        # Step 1: Extract carry names from the Pandas DataFrame
        carry_names_in_csv = set(df['name'])  # Extract the 'name' column from the DataFrame and convert it to a set

        # Step 2: Retrieve all carry names from the database
        carry_names_in_db = set(Carry.objects.values_list('name', flat=True))

        # Step 3: Identify carry names in the database that are not in the DataFrame
        carries_to_delete = carry_names_in_db - carry_names_in_csv

        # Step 4: Delete the carries from the database that are not in the DataFrame
        if carries_to_delete:
            Carry.objects.filter(name__in=carries_to_delete).delete()
            self.stdout.write(self.style.WARNING(f"Deleted {len(carries_to_delete)} carry entries."))
            for carry in carries_to_delete:
                print(f"- {carry}")
            print("\n")

    def create_or_update_superuser_rating(self, row):
        # Retrieve carry
        carry_qs = Carry.objects.filter(name=row["name"])
        if carry_qs.exists():
            carry = carry_qs.first() 
        else:
            raise ValidationError("This carry should exist at this point")

        # Retrieve the superuser
        superuser = CustomUser.objects.filter(is_superuser=True).first()

        if not superuser:
            raise ObjectDoesNotExist("Superuser not found. Please ensure a superuser exists.")

        superuser_rating = UserRating.objects.filter(user=superuser, carry=carry)

        try:
            if superuser_rating.exists():
                # If the UserRating exists, get the instance
                user_rating = superuser_rating.first()

                # Compare the fields of the existing instance with the row data
                fields_to_check = [
                    "newborns", "legstraighteners", "leaners", "bigkids", "feeding",
                    "quickups", "pregnancy", "difficulty", "fancy"
                ]

                updated = False

                # Check each field for changes
                for field in fields_to_check:
                    if getattr(user_rating, field) != row[field]:
                        setattr(user_rating, field, row[field])  # Update the field
                        updated = True

                user_rating.save()  # Save only if there were updates

                if updated:
                    self.stdout.write(self.style.SUCCESS(f"- Updated {row['name']} in UserRating model"))
                    return 0, 1

                return 0, 0

            else:
                # If the entry does not exist, create a new UserRating instance
                UserRating.objects.create(
                    user=superuser,
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
                )

                self.stdout.write(self.style.SUCCESS(f"- Created {row['name']} in UserRating model."))
                return 1, 0

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error creating {row['name']}: {str(e)}"))
            return 0, 0

    def create_or_update_carry(self, row):
        # Try to find the Carry instance by name
        carry_qs = Carry.objects.filter(name=row["name"])

        try:
            if carry_qs.exists():
                carry = carry_qs.first()  # Get the instance from the queryset

                # Compare the fields of the existing instance with the row data
                fields_to_check = [
                    "title", "longtitle", "size", "shoulders", "layers", "mmposition",
                    "videotutorial", "videoauthor", "videotutorial2", "videoauthor2",
                    "videotutorial3", "videoauthor3", "position", "description",
                    "pretied", "rings", "pass_horizontal", "pass_cross", "pass_reinforcing_cross",
                    "pass_reinforcing_horizontal", "pass_poppins", "pass_ruck", "pass_sling",
                    "pass_kangaroo", "other_chestpass", "other_bunchedpasses", "other_shoulderflip",
                    "other_twistedpass", "other_waistband", "other_legpasses", "other_s2s",
                    "other_eyelet", "other_poppins", "other_sternum", "finish",
                ]

                updated = False
                # Check each field for changes
                for field in fields_to_check:
                    if getattr(carry, field) != row[field]:
                        setattr(carry, field, row[field])  # Update the field
                        updated = True
                
                if updated:
                    carry.save()  # Save only if there were updates
                    self.stdout.write(self.style.SUCCESS(f"- Updated {row['name']} in Carry model"))
                    
                    return 0, 1
                else:
                    return 0, 0
            else:
                # If the entry does not exist, create a new Carry instance
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
                    finish=row["finish"],
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

                self.stdout.write(self.style.SUCCESS(f"- Created {row['name']} in Carry model."))

                return 1, 0

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error creating {row['name']}: {str(e)}"))
            return 0, 0


    def handle(self, *args, **kwargs):

        uploaded = 0
        updated = 0
        su_uploaded = 0
        su_updated = 0

        csv_file = kwargs['csv_file']

        table = self.read_carry_csv(csv_file)

        # Delete carries in db but not in csv_file
        self.delete_carries_not_in_file(table)

        # Create or update entries in Carry
        for _, row in table.iterrows():
            carry_uploaded, carry_updated = self.create_or_update_carry(row)

            uploaded += carry_uploaded
            updated += carry_updated

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully loaded {uploaded} carries to Carry model.'))
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated} carries in Carry model.'))
                
        # Create or update entries in UserRating for superuser
        for _, row in table.iterrows():
            su_carry_uploaded, su_carry_updated = self.create_or_update_superuser_rating(row)

            su_uploaded += su_carry_uploaded
            su_updated += su_carry_updated

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully loaded {su_uploaded} carries to UserRating model.'))
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {su_updated} carries in UserRating model.'))
