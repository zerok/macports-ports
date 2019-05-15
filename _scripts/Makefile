.PHONY: clean all dependencies check_updates

VENV := .macports-ports-venv

all: dependencies

$(VENV):
	python3 -m venv $@

dependencies: $(VENV)
	( \
	source $(VENV)/bin/activate; \
	pip install -r requirements.txt; \
	)

clean:
	rm -rf $(VENV)

# Script targets

check_updates:
	@( \
	source $(VENV)/bin/activate; \
	python update_check.py; \
	)

