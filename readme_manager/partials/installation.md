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

--------------------------

Use these CELERY settings

``` 
CELERY_BROKER_URL = config("RABBIT_MQ_URL")
CELERY_RESULT_BACKEND = config("REDIS_CLOUD_URL")
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
```


CELERY_RESULT_BACKEND have been commented, because we have used ```task.apply_async()``` instead of ```task.delay()```
with websockets for sending notification, django-db as a backend is synchronous
and thus gives error, Hence we have to use redis or other resources which primarily 
supports asynchronous work flow.

and we are explicitly passing backend=redis_url  while creating Celery app so it overrides CELERY_RESULT_BACKEND in settings.py

---

Creating Async App - create a file named celery.py in project directory.
``` 
import os

from celery import Celery
from celery.schedules import crontab
from decouple import config

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'borcelle_crm.settings')

redis_url = config("REDIS_CLOUD_URL")

app = Celery('borcelle_crm', broker=redis_url, backend=redis_url, include=['tasks.tasks'])

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


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

```

Run Server
```bash
  python manage.py runserver

  or 

  daphne -b 0.0.0.0 -p [PROJECT_DOCKER_PORT] [JENKINS PROJECT NAME].asgi:application
```
Use these CACHE settings

```python
if not DEBUG:
    CHANNEL_LAYERS = {
        'default': {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
        }
    }
else:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [(REDIS_CLOUD_URL)],
            },
        },
    }

```

Use these Channels Settings

```python
if not DEBUG:
    CHANNEL_LAYERS = {
        'default': {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
        }
    }
else:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [(config('REDIS_CLOUD_URL'))],
            },
        },
    }
```

[STATIC_FILES]

## Custom Django Management Commands

[DJANGO_COMMANDS]