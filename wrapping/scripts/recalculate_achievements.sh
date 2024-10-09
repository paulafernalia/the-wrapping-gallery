# Set the path to your Django project
PROJECT_DIR="$(dirname "$(dirname "$(realpath "$0")")")"  # Moves two directories up
PYTHON="$PROJECT_DIR/../venv/bin/python"  # Adjust this to your Python executable path

# Set the settings module for Django
DJANGO_SETTINGS_MODULE="wrapping.settings.production"  # Update with your actual settings module

# Navigate to the project directory
cd "$PROJECT_DIR" || { echo "Failed to navigate to project directory"; exit 1; }  # Exit if the directory change fails

# Create a timestamp for the log file name
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

# Define the log file name with timestamp
LOG_FILE="$PROJECT_DIR/logs/recalculate_timely_achievements$TIMESTAMP.log"

# Create the logs directory if it doesn't exist
mkdir -p "$PROJECT_DIR/logs"

# Run the recalculate_achievements management command and output to the log file
if ! $PYTHON manage.py recalculate_timely_achievements --settings=$DJANGO_SETTINGS_MODULE > "$LOG_FILE" 2>&1; then
    echo "Error occurred while recalculating achievements. Check $LOG_FILE for details."
    exit 1
fi

# Keep the last 10 log files
find "$PROJECT_DIR/logs" -type f -name "recalculate_timely_achievements*.log" -mtime +365 -exec rm {} \;

echo "Recalculation of achievements completed: $LOG_FILE, and old logs deleted."
