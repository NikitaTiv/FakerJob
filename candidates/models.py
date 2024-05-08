from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.urls import reverse


class Tag(models.Model):
    tag = models.CharField(max_length=20, unique=True, db_index=True)


class FakeManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_fake=True)


class RealManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_fake=False)


class Candidate(AbstractUser):
    GENDER_CHOICES = [(0, 'Male'), (1, 'Female')]

    email = models.EmailField(max_length=128, unique=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True)
    about = models.CharField(max_length=512, blank=True, default='')
    country = CountryField(null=True)
    is_fake = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='tags')

    objects = models.Manager()
    real_objects = RealManager()
    fake_objects = FakeManager()

    def __str__(self) -> str:
        return f'User: {self.pk} ({self.first_name} {self.last_name})'

    def get_absolute_url(self):
        return reverse('profile', self.pk)
