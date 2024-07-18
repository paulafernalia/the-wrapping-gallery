# Makefile

# Variables
PYTHON = python
MANAGE = manage.py

# Targets
.PHONY: run

runserver:
	$(PYTHON) $(MANAGE) runserver

# Every time we make changes in models.py, we have to make migrations
# and then migrate. Note that you may have to delete your existing
# entries or modify them if they don't fit in with the new
# database structure.
makemigrations:
	$(PYTHON) $(MANAGE) makemigrations

migrate:
	$(PYTHON) $(MANAGE) migrate

shell:
	$(PYTHON) $(MANAGE) shell
