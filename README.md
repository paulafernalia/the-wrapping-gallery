# The Wrapping Gallery

This is a project for a website with content related to babywearing with woven wraps created using python/Django and JavaScript.

The production environment uses a PostgreSQL database hosted in Supabase, the development environment uses a SQLite database. Both the development and the production environment use images stored in a S3 bucket in Supabase. When environment variables describing the connection details to the Supabase S3 bucket are not available, the app will use default images in the project's media folder.

To run the app in development mode, follow these steps:

1. Clone this repo.
2. Set up the required environment variables in a file called `.env.dev` (see below)
3. Run `docker compose -f docker-compose.dev.yml up --build -d`
4. Open http://0.0.0.0:8000 in a browser.
5. Run `docker compose down` to stop running the app and remove the Docker container.

The `.env` files must be at the same level as `manage.py` and list the following variables:

```
DB_NAME=xxxx
DB_USER=xxxx
DB_PASSWORD=xxxx
DB_HOST=xxxx
DB_PORT=xxxx

SECRET_KEY=xxxx

DJANGO_SETTINGS_MODULE=xxxx
DJANGO_ALLOWED_HOSTS=xxxx

SUPABASE_URL=xxxx
SERVICE_ROLE_KEY=xxxx

SUPABASE_COVER_BUCKET=carrycovers
SUPABASE_MISC_BUCKET=misc
SUPABASE_TUTORIAL_BUCKET=tutorials
```
