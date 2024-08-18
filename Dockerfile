FROM python:3.10.7

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8014

CMD bash -c "python manage.py collectstatic --noinput && daphne borcelle_crm.asgi:application -b 0.0.0.0 --port 8014 & celery -A borcelle_crm.celery worker -l info & celery -A borcelle_crm beat -l INFO"