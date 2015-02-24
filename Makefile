.PHONY: requirements

PROJECT_NAME = $(shell basename $(PWD))
PROJECT_NAME_UPPER = $(shell echo $(PROJECT_NAME) | tr [:lower:] [:upper:])
DEFAULT_VIRTUALENV = var/env
# Possible virtualenv if virtualenvwrapper is used
POSSIBLE_VIRTUALENV = $(WORKON_HOME)/$(PROJECT_NAME)
# Use possible virtualenv if it exists and virtualenvwrapper is used, otherwise use default one
VIRTUALENV = $(if $(and $(WORKON_HOME), $(wildcard $(POSSIBLE_VIRTUALENV))),$(POSSIBLE_VIRTUALENV),$(DEFAULT_VIRTUALENV))
PIP = $(VIRTUALENV)/bin/pip
PYTHON = $(VIRTUALENV)/bin/python

BS=\033[1m
BE=\033[0m
BSU=\033[1;4m
BLUE=\033[34m
CYAN=\033[36m
GREEN=\033[32m
MAGENTA=\033[35m
RED=\033[31m
WHITE=\033[37m
YELLOW=\033[33m
PREFIX=$(GREEN)$(BS)=>$(BE)$(WHITE)

default: env settings requirements syncdb

env:
	@echo "$(PREFIX) Creating virtual environment within \"$(YELLOW)$(BS)$(DEFAULT_VIRTUALENV)$(BE)$(white)\" directory"
	@virtualenv -q $(DEFAULT_VIRTUALENV)

settings:
	@echo "$(PREFIX) Local settings module preparation"
	@cp $(PROJECT_NAME)/settings/dev.py $(PROJECT_NAME)/settings/local.py
	@echo "$(PREFIX) Do not forget to edit it at $(YELLOW)$(BS)$(PROJECT_NAME)/settings/local.py$(BE)$(white)"

requirements:
	@echo "$(PREFIX) Installing requirements"
	@$(PIP) install -Uqr requirements.txt

requirements-upgrade:
	@echo "$(PREFIX) Upgrading requirements"
	@$(PIP) freeze | cut -d = -f 1 | xargs $(PIP) install -U

syncdb:
	@echo "$(PREFIX) Syncing and migrating database"
	@$(PYTHON) manage.py syncdb --noinput
	@echo "$(PREFIX) Run migrations."
	@$(PYTHON) manage.py migrate

run:
	@$(PYTHON) manage.py runserver

clean:
	@echo "$(PREFIX) Cleaning *.pyc files"
	@find . -name "*.pyc" -exec rm -f {} \;

static:
	@echo "$(PREFIX) Run collect static."
	@$(PYTHON) manage.py collectstatic --noinput

test:
	@$(PYTHON) manage.py test --noinput
