import json
import time
from random import random

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from celery_progress.backend import ProgressRecorder
from celery_progress.websockets.backend import WebSocketProgressRecorder
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from mailjet_rest import Client

mailjet = Client(auth=(settings.MAIL_JET_API_KEY, settings.MAIL_JET_API_SECRET), version='v3.1')


@shared_task(bind=True)
def send_mail_func(self):
    users = get_user_model().objects.all()
    for user in users:
        # mail_subject = "Hi! Celery Testing"
        # message = "You have received this email as a test message from CLOCK WORK Reminder & Notes"
        # to_email = user.email
        # send_mail(
        #     subject=mail_subject,
        #     message=message,
        #     from_email=settings.EMAIL_HOST_USER,
        #     recipient_list=[to_email],
        #     fail_silently=True,
        # )

        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "admin@arpansahu.me",
                        "Name": "Clock Works"
                    },
                    "To": [
                        {
                            "Email": user.email,
                            "Name": "Dear User"
                        }
                    ],
                    "Subject": "Hi! Celery Testing",
                    "TextPart": "You have received this email as a test message from CLOCK WORK Reminder & Notes",
                    "HTMLPart": f"<h3>Dear {user.email}, welcome to <a href='https://www.arpansahu.me/'>Clock Works</a>!</h3><br />May the delivery force be with you!<br>Message: You have received this email as a test message from CLOCK WORK Reminder & Notes",
                    "CustomID": f"{user.email}"
                }
            ]
        }
        result = mailjet.send.create(data=data)
    return "Done"


@shared_task(bind=True)
def send_mail_task(self, emails, headline, content):
    progress_recorder = ProgressRecorder(self)
    for email_no in range(len(emails)):
        # mail_subject = headline
        # message = content
        # send_mail(
        #     subject=mail_subject,
        #     message=message,
        #     from_email=settings.EMAIL_HOST_USER,
        #     recipient_list=[emails[email_no]],
        #     fail_silently=True,
        # )

        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "admin@arpansahu.me",
                        "Name": "Clock Works"
                    },
                    "To": [
                        {
                            "Email": emails[email_no],
                            "Name": "Dear User"
                        }
                    ],
                    "Subject": headline,
                    "TextPart": content,
                    "HTMLPart": f"<h3>Dear {emails[email_no]}, welcome to <a href='https://www.arpansahu.me/'>Clock Works</a>!</h3><br />May the delivery force be with you!<br>Message: {content}",
                    "CustomID": f"{emails[email_no]}"
                }
            ]
        }
        result = mailjet.send.create(data=data)

        progress_recorder.set_progress(email_no + 1, len(emails), f'Sending Notes to {emails[email_no]}')

    return "Done"


@shared_task(bind=True)
def send_mail_task_with_schedule(self, emails, headline, content):
    for email_no in range(len(emails)):
        # mail_subject = headline
        # message = content
        # send_mail(
        #     subject=mail_subject,
        #     message=message,
        #     from_email=settings.EMAIL_HOST_USER,
        #     recipient_list=[emails[email_no]],
        #     fail_silently=True,
        # )

        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "admin@arpansahu.me",
                        "Name": "Clock Works"
                    },
                    "To": [
                        {
                            "Email": emails[email_no],
                            "Name": "Dear User"
                        }
                    ],
                    "Subject": headline,
                    "TextPart": content,
                    "HTMLPart": f"<h3>Dear {emails[email_no]}, welcome to <a href='https://www.arpansahu.me/'>Clock Works</a>!</h3><br />May the delivery force be with you!<br>Message: {content}",
                    "CustomID": f"{emails[email_no]}"
                }
            ]
        }
        result = mailjet.send.create(data=data)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification_broadcast",
        {
            'type': 'send_notification',
            'message': json.dumps(f"Mail send to {emails} with headline {headline}")
        }
    )
    return "Done"


@shared_task(bind=True)
def ws_task(self, number):
    progress_recorder = WebSocketProgressRecorder(self)
    for i in range(number):
        time.sleep(.1)
        progress_recorder.set_progress(i + 1, number)
    return int(random() * 1000)


@shared_task(bind=True)
def web_socket_send_mail_task(self, emails, headline, content):
    progress_recorder = WebSocketProgressRecorder(self)
    for email_no in range(len(emails)):
        # mail_subject = headline
        # message = content
        # send_mail(
        #     subject=mail_subject,
        #     message=message,
        #     from_email=settings.EMAIL_HOST_USER,
        #     recipient_list=[emails[0]],
        #     fail_silently=True,
        # )
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "admin@arpansahu.me",
                        "Name": "Clock Works"
                    },
                    "To": [
                        {
                            "Email": emails[email_no],
                            "Name": "Dear User"
                        }
                    ],
                    "Subject": headline,
                    "TextPart": content,
                    "HTMLPart": f"<h3>Dear {emails[email_no]}, welcome to <a href='https://www.arpansahu.me/'>Clock Works</a>!</h3><br />May the delivery force be with you!<br>Message: {content}",
                    "CustomID": f"{emails[email_no]}"
                }
            ]
        }
        result = mailjet.send.create(data=data)
        progress_recorder.set_progress(email_no + 1, len(emails), f'Sending Notes to {emails[email_no]}')

    return "Done"
