Installing Pre requisites
```bash
  pip install -r requirements.txt
```

Create .env File and don't forget to add .env to gitignore
```bash
  add variables mentioned in .env.example
```

Making Migrations and Migrating them.
```bash
  python manage.py makemigrations
  python manage.py migrate
```
Run update_data Command
```
  python manage.py update_data
```
Creating Super User
```bash
  python manage.py createsuperuser
```

Installing Redis On Local (For ubuntu) for other Os Please refer to their website https://redis.io/
```bash
  curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
  echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
  sudo apt-get update
  sudo apt-get install redis
  sudo systemctl restart redis.service
```

to check if its running or not
```bash
  sudo systemctl status redis
```

Installing RabbitMQ On Local (For ubuntu) for other Os Please refer to their website https://redis.io/
```bash
  sudo apt-get update
  sudo apt-get install curl gnupg apt-transport-https
  curl -fsSL https://packagecloud.io/rabbitmq/rabbitmq-server/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/rabbitmq-archive-keyring.gpg
  echo "deb [signed-by=/usr/share/keyrings/rabbitmq-archive-keyring.gpg] https://packagecloud.io/rabbitmq/rabbitmq-server/ubuntu/ $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/rabbitmq.list
  sudo apt-get update
  sudo apt-get install rabbitmq-server
  sudo systemctl enable rabbitmq-server
  sudo systemctl start rabbitmq-server
```

to check if its running or not
```bash
  sudo systemctl status rabbitmq-server
```

Use these CELERY settings

``` 
CELERY_BROKER_URL = REDIS_CLOUD_URL
CELERY_RESULT_BACKEND = RABBIT_MQ_URL
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_TASK_DEFAULT_QUEUE = 'borcelle_crm_queue'
```

Creating Async App - create a file named celery.py in project directory.
``` 
import os

from celery import Celery
from celery.schedules import crontab
from decouple import config

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'borcelle_crm.settings')

app = Celery('borcelle_crm')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {
    'send-mail-every-day-at-8': {
        'task': 'send_email_app.tasks.send_mail_func',
        'schedule': crontab(hour=0, minute=38),
        # 'args' : (2,)
    }
}
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
```

Run Server
```bash
  python manage.py runserver

  or 

  uvicorn --host 0.0.0.0 -port [PROJECT_DOCKER_PORT] [JENKINS PROJECT NAME].asgi:application
```

[STATIC_FILES]

[CACHE]

[CHANNELS]

[SENTRY]

## Custom Django Management Commands

[DJANGO_COMMANDS]