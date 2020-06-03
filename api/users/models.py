from django.db import models
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField


class User(AbstractUser):
    birth_date = models.DateTimeField(null=True, blank=True)
    phone_number = PhoneField(null=True, blank=True, help_text='Your phone number')



