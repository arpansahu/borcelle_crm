from django.db import models

# Create your models here.
from account.models import Account
from borcelle_crm.models import AbstractBaseModel


class Contacts(AbstractBaseModel):
    name = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    gst = models.CharField(max_length=15)
    automated_reminders = models.IntegerField(default=0)
    country_code = models.CharField(max_length=5)
    phone = models.CharField(max_length=15)
    email = models.EmailField(verbose_name="email", max_length=60)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
