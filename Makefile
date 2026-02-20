EXPERIMENTS := $(wildcard a-*)
RUN := uv run --dev
TARGETS := data format lint test typecheck

.ONESHELL:

.PHONY: $(TARGETS) $(EXPERIMENTS)

all:
	$(error Give an experiment name or one of: $(TARGETS))

data: data/diamonds.csv data/urls.csv

data/diamonds.csv:
	mkdir -p data
	curl https://raw.githubusercontent.com/BahramJannesar/DiamondsMachineLearning/refs/heads/master/Datasets/diamonds_ready_for_ML.csv >$@

data/urls.csv:
	mkdir -p data
	curl https://archive.ics.uci.edu/static/public/967/phiusiil+phishing+url+dataset.zip | funzip >$@

format:
	$(RUN) ruff format a-*
	$(RUN) ruff check --select I --fix a-*

lint:
	$(RUN) ruff check a-*

test: lint typecheck

typecheck:
	$(RUN) mypy --scripts-are-modules a-*

$(EXPERIMENTS):
	uv run ./$@
