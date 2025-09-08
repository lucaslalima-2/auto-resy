VENV_NAME=venv

.PHONY: setup run clean

setup:
	python3 -m venv $(VENV_NAME)
	$(VENV_NAME)/bin/pip install --upgrade pip
	$(VENV_NAME)/bin/pip install -r requirements.txt
	$(VENV_NAME)/bin/python -m playwright install

run:
	$(VENV_NAME)/bin/python app.py

clean:
	rm -rf $(VENV_NAME)

freeze:
	$(VENV_NAME)/bin/pip freeze > requirements.txt