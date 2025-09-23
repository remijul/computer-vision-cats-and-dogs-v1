SHELL := /bin/bash
VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

env:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements/base.txt

activate:
	@echo "Run: source $(VENV)/bin/activate"
	

clear :
	rm -rf $(VENV)


