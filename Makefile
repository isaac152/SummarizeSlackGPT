SHELL := /bin/bash

linter:
	pre-commit run -a

create-env:
	python -m venv env && source ./env/bin/activate

build-dev: create-env
	python -m pip install -r requirements/dev.txt && pre-commit install 

dev:
	python -m app

build-prod: create-env
	python -m pip install -r requirements/base.txt

create-env-file:
	cp -n .env.example .env
