import datetime
import json

from asgiref.sync import sync_to_async
from django.http import HttpResponse
from django.shortcuts import render
from braces import views

# Create your views here.
from django.views import View
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from manager.models import Contacts, Message
from .tasks import web_socket_send_mail_task
from celery_progress.backend import ProgressRecorder


class ScheduleMail(views.JSONResponseMixin, views.AjaxResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        headline = request.POST.get('headline')
        emails = request.POST.get('emails').split(' ')
        content = request.POST.get('content')
        date_time = request.POST.get('datetime')
        try:
            date = datetime.datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%S')
        except:
            date = datetime.datetime.strptime(date_time, '%Y-%m-%dT%H:%M')
        contact_id = int(request.POST.get('contact_id'))
        print(emails)

        try:
            contact = Contacts.objects.get(id=contact_id)
            message = Message(message=content, contact=contact, scheduled=True)
            message.save()
            schedule, created = CrontabSchedule.objects.get_or_create(hour=date.hour, minute=date.minute,
                                                                      day_of_month=date.day, timezone='Asia/Kolkata',
                                                                      month_of_year=date.month)
            task = PeriodicTask.objects.create(crontab=schedule, name="schedule_mail_task_"
                                                                      + str(len(PeriodicTask.objects.all())),
                                               task='send_email_app.tasks.send_mail_task_with_schedule',
                                               args=json.dumps((emails, headline, content, message.id))
                                               )
            return self.render_json_response({'status': 'Success', 'message': 'Reminder Scheduled'}, status=200)
        except Exception as e:
            print("Error occured:", e)
            return self.render_json_response({'status': 'Failed', 'message': "Reminder Can't be Scheduled"}, status=400)


class WebSocketSendMail(views.JSONResponseMixin, views.AjaxResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        headline = request.POST.get('headline')
        emails = request.POST.get('emails').split(' ')
        content = request.POST.get('content')
        contact_id = int(request.POST.get('contact_id'))
        print(emails)
        try:
            contact = Contacts.objects.get(id=contact_id)
            message = Message(message=content, contact=contact)
            message.save()
            task = web_socket_send_mail_task.apply_async(args=[emails, headline, content, message.id])
            return self.render_json_response({"status": "Success", "message": "Notes Send", "task_id": task.task_id},
                                             status=200)
        except Exception as e:
            print(f"inside Exception {e}")
            return self.render_json_response({"status": "Failed", "message": "Notes Can't be Sent"}, status=400)
