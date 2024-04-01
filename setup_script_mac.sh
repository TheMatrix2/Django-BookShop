#!/bin/bash

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew install python@3.10

export PATH="/usr/local/opt/python@3.10/bin:$PATH"

python3.10 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser --username=admin@example.ru --email=admin@example.ru

python manage.py runserver
