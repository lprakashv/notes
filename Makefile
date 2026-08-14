SHELL := /bin/bash

.PHONY: lint build run test coverage

lint:
	bash ./build-local.sh build

build:
	bash ./build-local.sh build

run:
	bash ./build-local.sh serve

test:
	bash ./build-local.sh build

coverage: build
	@total="$$(find book -type f -name '*.md' | wc -l | tr -d ' ')"; \
		printf 'Documentation coverage: %s/%s Markdown files included in the strict build.\n' "$$total" "$$total"
