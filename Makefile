.PHONY: check python-check ui-check

PYTHON ?= python
PNPM ?= pnpm

check: python-check ui-check

python-check:
	$(PYTHON) -m pytest -p no:cacheprovider
	$(PYTHON) -m ruff check src tests scripts

ui-check:
	$(PNPM) --dir frontend run build
