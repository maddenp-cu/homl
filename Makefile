RUN     := uv run --dev
TARGETS := data format lint test typecheck

.ONESHELL:

.PHONY: $(TARGETS)

all:
	$(error Valid targets are: $(TARGETS))

data: data/diamonds.csv data/urls.csv

data/diamonds.csv:
	mkdir -p data
	curl https://raw.githubusercontent.com/BahramJannesar/DiamondsMachineLearning/refs/heads/master/Datasets/diamonds_ready_for_ML.csv >$@

data/urls.csv:
	mkdir -p data
	curl https://archive.ics.uci.edu/static/public/967/phiusiil+phishing+url+dataset.zip | funzip >$@

format:
	$(RUN) ruff format
	$(RUN) ruff check --select I --fix

lint:
	$(RUN) ruff check

test: lint typecheck

typecheck:
	$(RUN) mypy .
