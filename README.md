# The Wrapping Gallery

This is a project for a website with content related to babywearing with woven wraps created using python/Django and JavaScript.

The production environment uses a PostgreSQL database hosted in Supabase, the development environment uses a SQLite database. Both the development and the production environment use images stored in a S3 bucket in Supabase. When environment variables describing the connection details to the Supabase S3 bucket are not available, the app will use default images in the project's media folder.

To set run the app in development mode, follow these steps:

1. Clone this repo.
2. Navigate to the Django project folder: `cd wrapping`.
3. Install dependencies with `pip install -r requirements.txt`.
4. Create a SQLite development database with some initial data: `make setup-env-db`.
5. Run the app with `make runserver`.

Unit tests are run with `make test`.
