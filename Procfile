release: python manage.py migrate
web: daphne borcelle_crm.asgi:application --port $PORT --bind 0.0.0.0 -v2
celery: celery -A borcelle_crm.celery worker -l info
celerybeat: celery -A borcelle_crm beat -l INFO
celeryworker2: celery -A borcelle_crm.celery worker & celery -A borcelle_crm beat -l INFO & wait -n