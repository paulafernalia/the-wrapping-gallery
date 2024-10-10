#!/bin/bash

# Set the path to your Django project
PROJECT_DIR="$(dirname "$(dirname "$(realpath "$0")")")"  # Moves two directories up
PYTHON="$PROJECT_DIR/../venv/bin/python"  # Adjust this to your Python executable path
# Set the settings module for Django
DJANGO_SETTINGS_MODULE="wrapping.settings.production"  # Update with your actual settings module

# Navigate to the project directory
cd "$PROJECT_DIR" || { echo "Failed to navigate to project directory"; exit 1; }  # Exit if the directory change fails

# Create a timestamp for the backup file name
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

# Define the backup file name with timestamp
BACKUP_FILE="$PROJECT_DIR/backups/prod_db_backup_$TIMESTAMP.json"

# Create the backups directory if it doesn't exist
mkdir -p "$PROJECT_DIR/backups"

# Run the dumpdata command and output to the backup file
if ! $PYTHON manage.py dumpdata --settings=$DJANGO_SETTINGS_MODULE --indent 2 > "$BACKUP_FILE" 2>> "$PROJECT_DIR/backups/backup_errors.log"; then
    echo "Error occurred while creating backup. Check backup_errors.log for details."
    exit 1
fi

# Delete backups older than 10 days
find "$PROJECT_DIR/backups" -type f -name "*.json" -mtime +10 -exec rm {} \;

echo "Backup completed: $BACKUP_FILE, and old backups deleted."
