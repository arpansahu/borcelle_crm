import json
import time
from random import random

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from celery_progress.websockets.backend import WebSocketProgressRecorder
from celery import shared_task
from django.conf import settings
from mailjet_rest import Client

from manager.models import Message

mailjet = Client(auth=(settings.MAIL_JET_API_KEY, settings.MAIL_JET_API_SECRET), version='v3.1')




@shared_task(bind=True)
def send_mail_task_with_schedule(self, emails, headline, content, message):
    for email_no in range(len(emails)):

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
                    "HTMLPart": f"<h3>Dear {emails[email_no]}, Message: {content}",
                    "CustomID": f"{emails[email_no]}"
                }
            ]
        }
        result = mailjet.send.create(data=data)
        if result:
            message_obj = Message.objects.get(id=message)
            message_obj.success = True
            message_obj.save()
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
def web_socket_send_mail_task(self, emails, headline, content, message):
    progress_recorder = WebSocketProgressRecorder(self)
    for email_no in range(len(emails)):
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
                    "HTMLPart": f"<h3>Dear {emails[email_no]}, Message: {content}",
                    "CustomID": f"{emails[email_no]}"
                }
            ]
        }
        result = mailjet.send.create(data=data)
        if result:
            message_obj = Message.objects.get(id=message)
            message_obj.success = True
            message_obj.save()
        progress_recorder.set_progress(email_no + 1, len(emails), f'Sending Notes to {emails[email_no]}')
    return "Done"
