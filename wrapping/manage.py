#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from decouple import config


def main():
    """Run administrative tasks."""
    # Check if the test command is being run
    if "test" in sys.argv:
        # Automatically switch to test settings
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wrapping.settings.test")
    else:
        # Use the configured or default settings for other commands
        settings_module = config(
            "DJANGO_SETTINGS_MODULE", default="wrapping.settings.development"
        )
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
