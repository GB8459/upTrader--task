!#/usr/bin/env

exec > output.log 2>&1

python -m manage makemigrations
python -m manage migrate
python -m manage runserver
