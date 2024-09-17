# myapp/management/commands/check_static_files.py
from django.core.management.base import BaseCommand
from django.conf import settings
import os
from wrappinggallery.models import Carry  # Replace 'myapp' with your actual app name

class Command(BaseCommand):
    help = 'Check static files in the "illustrations" folder against database entries'

    def handle(self, *args, **kwargs):
        self.stdout.write('Checking static files against database entries...')

        # Determine the path to the "illustrations" folder inside the static directory
        illustrations_subfolder = 'wrappinggallery/illustrations'

        # Determine the static folder path, depending on environment (STATICFILES_DIRS in dev, STATIC_ROOT in prod)
        static_root = getattr(settings, 'STATIC_ROOT', None)

        file_names = []
        # In production: Walk through STATIC_ROOT to find the "illustrations" folder
        if static_root:
            illustrations_path = os.path.join(static_root, illustrations_subfolder)
            if os.path.exists(illustrations_path):
                for root, dirs, files in os.walk(illustrations_path):
                    file_names.extend(files)

        self.check_static_files_in_db(file_names)
        self.check_dark_variants(file_names)

    def check_static_files_in_db(self, file_names):
        # Normalize filenames to remove ".png" and "_dark.png"
        normalized_file_names = [self.normalize_file_name(file) for file in file_names]

        # Query all entries in the Carry model
        carry_entries = Carry.objects.values_list('name', flat=True)

        # Check which files are not present in the database
        missing_in_db = []
        for i, file in enumerate(normalized_file_names):
            if file not in carry_entries and "placeholder" not in file:
                missing_in_db.append(file_names[i])

        # Output results to the console (or log them)
        if missing_in_db:
            self.stdout.write(f"WARNING: Some files not in DB: {missing_in_db}")
        else:
            self.stdout.write("OK: All illustrations have corresponding database entries.")

    def normalize_file_name(self, file_name):
        """
        Normalize file names by removing the "_dark" part and the ".png" extension.
        """
        # Remove the _dark suffix if it exists
        if file_name.endswith('_dark.png'):
            return file_name[:-9]  # Remove '_dark.png'
        elif file_name.endswith('.png'):
            return file_name[:-4]  # Remove '.png'
        return file_name  # Return the file name as is if it doesn't match the patterns


    def check_dark_variants(self, file_names):
        missing_dark_files = []

        for file_name in file_names:
            if file_name.endswith('.png') and 'dark' not in file_name:
                # Construct the expected dark file name
                dark_file_name = file_name.replace('.png', '_dark.png')
                
                # Check if the dark file exists in the list
                if dark_file_name not in file_names:
                    missing_dark_files.append(dark_file_name)
        
        if missing_dark_files:
            self.stdout.write("WARNING: The following dark files are missing:")
            for missing_file in missing_dark_files:
                self.stdout.write(missing_file)

        else:
            self.stdout.write("OK: All illustrations have a dark counterpart.")
