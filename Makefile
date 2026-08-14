SHELL := /bin/bash
PYTHON_BIN ?= python3
NOTES_SCRIPT := skills/cultivate-notes/scripts/notes.py

.PHONY: lint build run test coverage notes-list notes-check notes-test

lint:
	bash ./build-local.sh lint

build:
	bash ./build-local.sh build

run:
	bash ./build-local.sh run

test:
	bash ./build-local.sh test

coverage:
	bash ./build-local.sh coverage

notes-list:
	$(PYTHON_BIN) $(NOTES_SCRIPT) --repo . scan

notes-check:
	$(PYTHON_BIN) $(NOTES_SCRIPT) --repo . lint

notes-test:
	$(PYTHON_BIN) -m unittest discover skills/cultivate-notes/scripts -p 'test_*.py'
