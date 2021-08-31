VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

install: $(VENV)/bin/activate
	mkdir ./data

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt
