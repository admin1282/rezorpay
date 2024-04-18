from split_settings.tools import include
from os import environ

include('components/common.py')


ENV = environ.get('DJANGO_ENV')

if ENV == "production":
    include('environments/production.py')
