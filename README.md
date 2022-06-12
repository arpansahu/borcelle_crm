
# Borcelle CRM | Django Redis/RabbitMQ Celery

This project provides following features

-Implemented CRM
    
1. A user can register and start adding his contacts separately which are private to him
2. You can do CRUD operation with your contacts
3. Message your contacts via portal which will be emailed to them to their email.
4. Check history of messages
5. Email Verification before user can login


-Implemented Celery and Redis to Take Notes and Email it.
    
1. Used MailJet in Production to send Emails, at first Gmail with SMTP was using. Since heroku don't allow SMTP activities in the server, MailJet was used 
2. You can see the progress of the task in frontend
3. Progress Bar is Implemented with Ajax as well as Channels


-Implemented Celery Beat to Schedule Emails as Reminders

1. Used Celery beat to Schedule Reminder Emails
2. used asyncio inside Signals Code to avoid interference with sync_to_async
3. As soon as task is completed a notification is send to user about its completion

-Broadcast Notifications using Web Sockets and Channels

-Deployed on Heroku

1. Used Heroku Postgres 
2. Used Daphene
3. Used REDIS-CLOUD Sever, provided by heroku add-ons

## What is Redis, Celery, Celery Beat, Web Sockets, Channels, Signals, Ajax and working ?
In the below image I will try to explain everything.

![alt text](https://github.com/arpansahu/borcelle_crm/blob/master/explanation.png?raw=true)

## Working:-

1. When a user wants to take notes and want it to email-ed. Then from Django app we send 
    a request to Django View to create and Send a task to Redis/RabbitMQ broker. Then 
    broker will be passing this task to celery. Moreover, since while creating a task we 
    used celery results to save the progress in CELER_RESULT_BACKEND (django-db or redis or rabbitmq).
    So while the task is being executed user can see progress bar via two methods:

    - Using Ajax Call: While the process is not completed you can continuously hit the 
      endpoint to check status fo the task. which eventually increase your server load.
    - Using Web Sockets and channels: As soon as you load the web page you make a web socket 
      protocol connection to the server via handshaking and once the connection is established
      your server can directly send messages to frontend without request from the user end.
      This channel layer is also using Redis for Quick Response. So as soon as there are any changes
      to status of task it is notified to channel and if user is still connected to the channels, will
      be able to see the results in progress bar.

2. When a user wants to Schedule an Email as Reminder then, Via Django Application View, a cron task is created and that is 
   assigned to Celery Beat and as soon as the scheduled time arrived it pass task to broker, and then it is finally assigned 
   to celery which finishes the task and at the end of the task, a message is passed through channels to frontend to notify about the completion of task.

3. Admin can broadcast a Notification to all users using django channels and cron tab, admin can schedule the notification 
   at a particular time and then as soon as time arrives Celery Beat transfers task to Broker, and then it passes to Celery Workers.
   Moreover, the task focuses on sending notification through channels and web sockets so that users connected to particular channels 
   will be able to see the notifications.





## What is Django ?
Django is a Python-based free and open-source web framework that follows the model-template-view architectural pattern.

## What is Web Sockets ?

WebSocket is bidirectional, a full-duplex protocol that is used in the same scenario of client-server communication, unlike HTTP it starts from ws:// or wss://. It is a stateful protocol, which means the connection between client and server will keep alive until it is terminated by either party (client or server). After closing the connection by either of the client and server, the connection is terminated from both ends. 

## What is Channels?
Channels preserve the synchronous behavior of Django and add a layer of asynchronous protocols allowing users to write the views that are entirely synchronous, asynchronous, or a mixture of both. Channels basically allow the application to support “long-running connections”. It replaces Django’s default WSGI with its ASGI.

## What is Django Signals?
Django includes a “signal dispatcher” which helps decoupled applications get notified when actions occur elsewhere in the framework. In a nutshell, signals allow certain senders to notify a set of receivers that some action has taken place.

## What is Ajax?
Ajax is a set of web development techniques that uses various web technologies on the client-side to create asynchronous web applications. With Ajax, web applications can send and retrieve data from a server asynchronously without interfering with the display and behaviour of the existing page. 

## What is Celery ?
Celery is an asynchronous task queue/job queue based on distributed message passing. It is focused on real-time operation but supports scheduling as well.

Why is this useful?

1. Think of all the times you have had to run a certain task in the future. Perhaps you needed to access an API every hour. Or maybe you needed to send a batch of emails at the end of the day. Large or small, Celery makes scheduling such periodic tasks easy.
2. You never want end users to have to wait unnecessarily for pages to load or actions to complete. If a long process is part of your application’s workflow, you can use Celery to execute that process in the background, as resources become available, so that your application can continue to respond to client requests. This keeps the task out of the application’s context.

Working:
1. Celery requires message broker to store messages received from task generators or producers. For reading information of messages in task
  serialization is required which can be in json/pickle/yaml/msgpack it can be in compressed form as zlib, bzip2 or a cryptographic message.
2. A celery system consists of multiple workers and brokers, giving way to high availability and horizontal scaling.
3. When a celery worker is started using command ```celery -A [borcelle_crm(project name)].celery worker -l info```, a supervisor is started.
4. Which spawns child processes or threads and deals with all the bookkeeping stuff. The child processes or threads execute the actual task.
  This child process are also known as execution pool. By default, no of child process worker can spawn is equal to the no of CPU cores.
5. The size of execution pool determines the number of tasks your celery worker can process
   1. Worker ----- Pool ----- Concurrency 
   2. When you start a celery worker, you specify the pool, concurrency, autoscale etc. in the command 
   3. Pool - Decides who will actually perform the task -thread, child process, worker itself or else. 
   4. Concurrency: will decide the size of pool
   5. autoscale: to dynamically resize the pool based on load. The autoscaler adds more pool processes when there is work
     to do, and starts removing processes when the workload is low.
   6. ```celery -A <project>.celery worker --pool=preform --concurrency=5 --autoscale=10 3 -l info ``` 
    this command states to start a worker with 5 child processes which can be auto-scaled upto 10 and can be decreased upto 3.
6. Type of Pools: 
    1. prefork (multiprocessing) (default):
       1. Use this when CPU bound task
       2. By passes GIL (Global Interpreter Lock)
       3. The number of available cores limits the number of concurrent processes.
       4. That's why Celery defaults concurrency to no of CPU cores available.
       5. Command: ```celery A -<project>.celery worker -l info```
    2. solo (Neither threaded nor process-based)
        1. Celery don't support windows, so you can use this pool of running celery on Windows
        2. It doesn't create pool as it runs solo.
        3. Contradicts the principle that the worker itself does not process any tasks
        4. The solo pool runs inside the worker process.
        5. This makes the solo worker fast, But it also blocks the worker while it executes tasks.
        6. In this concurrency doesn't make any sense.
        7. Command ```celery A -<project>.celery worker --pool=solo -l info```
    3. threads (multi threading)
        1. due to GIL in CPython, it restricts to single thread so can't achieve real multithreading
        2. Not much official support
        3. Uses threading module of python
        4. Command ```celery A -<project>.celery worker --pool=threads -l info```
    4. gevent/eventlet (Green Threads)
       1. Uses Green thread which are user level threads so can be manipulated at code level 
       2. This can be used to get a thousand of HTTP get request to fetch from external REST APIs.
       3. The bottleneck is waiting for I/O operation to finish and not CPU.
       4. There are implementation differences between the eventlet and gevent packages
       5. Command ```celery A -<project>.celery worker --pool=[gevent/eventlet] worker -l info```
    5. by default ```celery A -<project>.celery worker -l info``` uses pool-prefork and concurrency -no of cores
    6. Difference between greenlets and threads -
       1. Python's threading library makes use of the system's native OS to schedule threads. This general-purpose scheduler is not always very efficient. 
       2. It makes use of Python's global interpreter lock to make sure shared data structures are accessed by only one thread at a time to avoid race conditions.
          CPython Interpreter, GIL, OS Greenlets emulate multi-threaded environments without relying on any native operating system capabilities.
          Greenlets are managed in application space and not in kernel space. In greenlets, no scheduler pre-emptively switching between your threads
          at any given moment. 
       3. Instead, your greenlets voluntarily or explicitly give up control to one another at specified points in your code. 
       4. Thus more scalable and efficient. Less RAM required.
       
## What is Redis ?
    
Redis is an in-memory data structure project implementing a distributed, in-memory key-value database with optional durability. 
The most common Redis use cases are session cache, full-page cache, queues, leaderboards and counting, publish-subscribe, and much more. in this case, we will use Redis as a message broker.

## What is RabbitMQ?
RabbitMQ is an open-source message-broker software that originally implemented the Advanced Message Queuing Protocol and has since been extended with a plug-in architecture to support Streaming Text Oriented Messaging Protocol, MQ Telemetry Transport, and other protocols. 

## Tech Stack

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Glossary/HTML5)
[![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Javascript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)](https://www.javascript.com/)
[![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/docs/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/docs/)
[![Celery](https://img.shields.io/badge/celery-%2337814A.svg?&style=for-the-badge&logo=celery&logoColor=white)](https://docs.celeryq.dev/en/stable/index.html)
[![RabbitMQ](https://img.shields.io/badge/rabbitmq-%23FF6600.svg?&style=for-the-badge&logo=rabbitmq&logoColor=white")](https://www.rabbitmq.com/)
[![Heroku](https://img.shields.io/badge/-Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)](https://heroku.com/)
[![Github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://www.github.com/)

## Demo

Available at: https://clock-works.herokuapp.com/

admin login details:--
username: arpansahu
password: showmecode
## License

[MIT](https://choosealicense.com/licenses/mit/)


## Installation

Installing Pre requisites
```bash
  pip install -r requirements.txt
```

Create .env File
```bash
  add variables mentioned in .env.example
```

Making Migrations and Migrating them.
```bash
  python manage.py makemigrations
  python manage.py migrate
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
```
  sudo systemctl status redis
```
--------------------------

Use these CELERY settings

``` 
CELERY_BROKER_URL = 'redis://localhost:6379'
# CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
```


CELERY_RESULT_BACKEND have been commented, because we have used ```task.apply_async()``` instead of ```task.dealy()```
with websockets for sending notification, django-db as a backend is synchronous
and thus gives error, Hence we have to use redis or other resources which primarily 
supports asynchronous work flow.


---

Creating Async App - create a file named celery.py in project directory.
``` 
import os

from celery import Celery
from celery.schedules import crontab
from decouple import config

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'borcelle_crm.settings')

redis_url = config("REDISCLOUD_URL")

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

set ASGI settings in settings.py
``` 
ASGI_APPLICATION = 'borcelle_crm.routing.application'
```

Uncomment Channel Layers Setting for Local Machine on settings.py
```bash
   CHANNEL_LAYERS = {
     'default': {
         'BACKEND': 'channels_redis.core.RedisChannelLayer',
         'CONFIG': {
             "hosts": [('127.0.0.1', 6379)],
         },
     },
   }
```
Comment Channel Layers Setting for Heroku on settings.py
```bash
   CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [config('REDISCLOUD_URL')],
        },
    },
  }
```

Run Server
```bash
  python manage.py runserver
```

## Deployment on Heroku

Installing Heroku Cli from : https://devcenter.heroku.com/articles/heroku-cli
Create your account in Heroku.

Inside your project directory

Login Heroku CLI
```bash
  heroku login

```

Create Heroku App

```bash
  heroku create [app_name]

```

Push Heroku App
```
    git push heroku master
```

Configure Heroku App
```bash
  heroku config:set GITHUB_USERNAME=joesmith

```
Configuring Django App for Heroku

Install whitenoise 
```
pip install whitenoise 
```

Include it in Middlewares.
```
MIDDLEWARE = [
    # ...
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # ...
]
```

Create Procfile and include this code snippet in it.
```
release: python manage.py migrate
web: daphne borcelle_crm.asgi:application --port $PORT --bind 0.0.0.0 -v2
celery: celery -A borcelle_crm.celery worker -l info
celerybeat: celery -A borcelle_crm beat -l INFO
celeryworker2: celery -A borcelle_crm.celery worker & celery -A borcelle_crm beat -l INFO & wait -n
```

In the above Procfile there are three workers required for web, celery and celery beat, but since heroku free
plan only allows upto 2 free dynos we have merged celery and celerybeat into celeryworker2
and from the admin panel of heroku app we can enable just the web and celeryworker2.

Comment down Database setting and install 

``` 
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME'),
#         'USER': config('DB_USER'),
#         'PASSWORD': config('DB_PASSWORD'),
#         'HOST': config('DB_HOST'),
#         'PORT': config('DB_PORT'),
#     }
# }
```
```
pip install dj-database-url
```

and add these lines below the commented Database settings
``` 
import dj_database_url
DATABASES = {'default': dj_database_url.config(default=config('DATABASE_URL'))}
```

Change CELERY_BROKER_URL from 
``` 
CELERY_BROKER_URL = 'redis://localhost:6379'
```
to
```
CELERY_BROKER_URL=config("REDISCLOUD_URL")
```
## Documentation

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Glossary/HTML5)
[![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Javascript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)](https://www.javascript.com/)
[![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/docs/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/docs/)
[![Celery](https://img.shields.io/badge/celery-%2337814A.svg?&style=for-the-badge&logo=celery&logoColor=white)](https://docs.celeryq.dev/en/stable/index.html)
[![RabbitMQ](https://img.shields.io/badge/rabbitmq-%23FF6600.svg?&style=for-the-badge&logo=rabbitmq&logoColor=white")](https://www.rabbitmq.com/)
[![Heroku](https://img.shields.io/badge/-Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)](https://heroku.com/)
[![Github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://www.github.com/)

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

REDISCLOUD_URL=

SECRET_KEY=

DEBUG=

ALLOWED_HOSTS=

EMAIL_USER=

EMAIL_PASS=

DATABASE_URL=

MAIL_JET_API_KEY=

MAIL_JET_API_SECRET=

ALLOWED_HOSTS=

REDIS_URL=
