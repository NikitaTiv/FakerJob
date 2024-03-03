from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField


class Candidate(AbstractUser):
    GENDER_CHOICES = [(0, 'Male'), (1, 'Female')]

    email = models.EmailField(max_length=128, unique=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True)
    about = models.CharField(max_length=512, blank=True, default='')
    country = CountryField(null=True)
    is_fake = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'User: {self.pk} ({self.first_name} {self.last_name})'
