# The Wrapping Gallery

This is a project for a website with content related to babywearing with woven wraps created using python/Django and JavaScript.

The production environment uses a PostgreSQL database hosted in Supabase, the development environment uses a SQLite database. Both the development and the production environment use images stored in a S3 bucket in Supabase. When environment variables describing the connection details to the Supabase S3 bucket are not available, the app will use default images in the project's media folder.

To set run the app in development mode, follow these steps:

1. Clone this repo.
2. Create an environment with python3.12: `python3.12 -m venv venv`.
3. Activate the environment: `source venv/bin/activate`.
4. Navigate to the Django project folder: `cd wrapping`.
5. Install dependencies with `pip install -r requirements.txt`.
6. Create a SQLite development database with some initial data: `make setup-dev-db`.
7. Run the app with `make runserver`.

Unit tests are run with `make test`.
