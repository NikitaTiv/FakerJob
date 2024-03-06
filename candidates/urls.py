from django.urls import path

from candidates.views import index, profile


urlpatterns = [
    path('', index, name='home'),
    path('profile/', profile, name='profile')
]
