from django.contrib import admin

from candidates.models import Candidate  # noqa:F401


admin.site.register(Candidate)
