release: python manage.py migrate
web: daphne clock_work.asgi:application --port $PORT --bind 0.0.0.0 -v2
celery: celery -A clock_work.celery worker -l info
celerybeat: celery -A clock_work beat -l INFO
celeryworker2: celery -A clock_work.celery worker & celery -A clock_work beat -l INFO & wait -n