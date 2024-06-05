from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django_countries.fields import CountryField
from django.urls import reverse


class Tag(models.Model):
    tag = models.CharField(max_length=20, unique=True, db_index=True)

    def __str__(self) -> str:
        return self.tag


class FakeManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_fake=True)


class RealManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_fake=False)


class Candidate(AbstractUser):
    GENDER_CHOICES = [(0, 'Male'), (1, 'Female')]

    email = models.EmailField(max_length=128, unique=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    about = models.CharField(max_length=512, blank=True, default='')
    country = models.CharField(max_length=200,  null=True, choices=CountryField().choices + [('', 'Select Country')])
    is_fake = models.BooleanField(default=False, editable=False, verbose_name='fake status')
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='tags')

    objects = UserManager()
    real_objects = RealManager()
    fake_objects = FakeManager()

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return f'User: {self.pk} ({self.first_name} {self.last_name})'

    def get_absolute_url(self) -> str:
        return reverse('candidate_profile', kwargs={'candidate_id': self.pk})
