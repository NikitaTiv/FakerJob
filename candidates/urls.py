from django.urls import path

from candidates.views import index


urlpatterns = [
    path('', index, name='home')
]
