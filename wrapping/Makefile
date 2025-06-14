# Makefile

# Variables
PYTHON = python
MANAGE = manage.py
MYPROJ = wrapping
MYAPP = wrappinggallery

# Targets
.PHONY: run

runserver:
	$(PYTHON) manage.py runserver

# Every time we make changes in models.py, we have to make migrations
# and then migrate. Note that you may have to delete your existing
# entries or modify them if they don't fit in with the new
# database structure.
makemigrations:
	$(PYTHON) manage.py makemigrations

migrate:
	$(PYTHON) manage.py migrate

migrate-prod:
	$(PYTHON) manage.py migrate --settings=$(MYPROJ).settings.production 

# Command to check for missing ratings
check-ratings:
	$(PYTHON) manage.py check_ratings --settings=$(MYPROJ).settings.development

sync-dev-db:
	# Dump all data from the production database
	$(PYTHON) manage.py dumpdata --settings=$(MYPROJ).settings.production --indent 2 > all_data.json
	
	# Migrate the development database schema
	$(PYTHON) manage.py migrate --settings=$(MYPROJ).settings.development
	
	# Clear all data in the development database
	$(PYTHON) manage.py flush --settings=$(MYPROJ).settings.development --noinput
	
	# Load all data into the development database
	$(PYTHON) manage.py loaddata all_data.json --settings=$(MYPROJ).settings.development
	
	# Clean up temporary data file
	rm all_data.json

test:
	$(PYTHON) manage.py test

load-csv-data:
	$(PYTHON) manage.py load_csv_data initial_data.csv --settings=wrapping.settings.development

load-achievement-data:
	$(PYTHON) manage.py load_achievement_data --settings=wrapping.settings.development

dev-docker-down:
	docker compose -f docker-compose.dev.yml down -v

dev-docker-up:
	docker compose -f docker-compose.dev.yml up --build

ruff:
	ruff check
