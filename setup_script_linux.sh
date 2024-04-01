#!/bin/bash

# Установка Python 3.10
sudo apt-get update
sudo apt-get install -y python3.10

# Клонирование репозитория Django-приложения
git clone https://github.com/TheMatrix2/Django-BookShop.git djangoProject

# Переход в каталог приложения
cd djangoProject

# Создание виртуального окружения
python3.10 -m venv .venv

# Активация виртуального окружения
source .venv/bin/activate

# Установка зависимостей из requirements.txt
pip install -r requirements.txt

# Применение миграций Django
python manage.py migrate

# Создание суперпользователя Django
python manage.py createsuperuser --username=admin@example.ru --email=admin@example.ru

# Запуск Django-приложения
python manage.py runserver
