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

To run using docker in production mode:

1. Clone this repo
2. Run `docker compose up --build -d`
3. Open http://0.0.0.0:1337/ in a browser

To run the app, both with and without docker, you need an `.env` file at the same level as `manage.py` with the following variables:

```
DB_NAME=xxxx
DB_USER=xxxx
DB_PASSWORD=xxxx
DB_HOST=xxxx
DB_PORT=xxxx

SECRET_KEY=xxxx

DJANGO_SETTINGS_MODULE=wrapping.settings.production
DJANGO_ALLOWED_HOSTS=xxxx

SUPABASE_URL=xxxx
SERVICE_ROLE_KEY=xxxx

SUPABASE_COVER_BUCKET=carrycovers
SUPABASE_MISC_BUCKET=misc
SUPABASE_TUTORIAL_BUCKET=tutorials
```
