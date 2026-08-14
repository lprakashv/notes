SHELL := /bin/bash

.PHONY: lint build run test coverage

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
