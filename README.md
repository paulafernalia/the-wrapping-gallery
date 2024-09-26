# The Wrapping Gallery

This is a project for a website with content related to babywearing with woven wraps created using python/Django and JavaScript.

The production and development environments use a PostgreSQL database hosted in Supabase. This database contains a bunch of tables with data needed to run the app as well as a S3 bucket where tutorial images are stored.

To run the app in development mode, follow these steps:

1. Install [Docker](https://www.docker.com/get-started/).
2. Clone this repo.
3. Set up the required environment variables in a file called `.env.dev` (see below)
4. Run `docker compose -f docker-compose.dev.yml up --build -d`
5. To view on desktop: open http://0.0.0.0:8000 in a browser.
6. To view on mobile: open http://`<your-local-ip>`:8000/ on your phone. 
7. Run `docker compose -f docker-compose.dev.yml down` to stop running the app and remove the Docker container.

The `.env.dev` file must be at the same level as `manage.py` and list the following variables:

```
SECRET_KEY=<your-secret-key>

DJANGO_SETTINGS_MODULE=wrapping.settings.development

SUPABASE_URL=<SUPABASE_URL>
SUPABASE_TUTORIAL_BUCKET=<SUPABASE_TUTORIAL_BUCKET>
SERVICE_ROLE_KEY=<your-service-role-key>
DB_NAME=<DB_NAME>
DB_USER=<DB_USER>
DB_PASSWORD=<DB_PASSWORD>
DB_HOST=<DB_HOST>
DB_PORT=<DB_PORT>

EMAIL_HOST_USER=<EMAIL_HOST_USER>
EMAIL_HOST_PASSWORD=<EMAIL_HOST_PASSWORD>

```

To find `<your-local-ip>` execute `ifconfig` on your terminal (linux/macOS) and look for the "IPv4 Address" under the section for your active network connection.


If you create a database to test this in development, before running the `docker compose -f docker-compose.dev.yml up --build -d` for the first time, you must run `python manage.py createsuperuser` to create a superuser and then `python manage.py load_csv_data initial_data.csv` to load some initial data to the database.


## Licensing

This project is licensed under the GNU General Public License (GPL), version 3.0, except for the illustrations included in the repository.

### Illustrations

The illustrations included in this repository under `wrapping/wrappinggallery/static/wrappinggallery/illustrations` are not covered by the GPL license. These images are protected by copyright, and any use of them outside of this project requires explicit permission from the author. Please contact thewrappinggallery@gmail.com for more information.
