from django.db import models
from django.contrib.auth.models import User


class Candidate(models.Model):
    GENDER_CHOICES = [(0, 'Male'), (1, 'Female')]

    email = models.EmailField(max_length=128, unique=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True)
    about = models.CharField(max_length=512, null=True)
    is_fake = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='profiles', on_delete=models.CASCADE)

    def __str__(self) -> None:
        return f'User: {self.pk}({self.first_name} {self.second_name})'
