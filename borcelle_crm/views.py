from django.http import request, HttpResponse
from django.shortcuts import render
from django.views.generic import View
from .tasks import test_func


class Home(View):
    def get(self, *args, **kwargs):
        return render(self.request, template_name='old/Home.html', context={'room_name': "broadcast"})


class CeleryTest(View):
    def get(self, *args, **kwargs):
        test_func.delay()
        return HttpResponse("Done")
