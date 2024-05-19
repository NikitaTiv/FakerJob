from django.urls import path

from candidates.views import get_all_candidates, get_candidate_info


urlpatterns = [
    path('', get_all_candidates, name='candidate_list'),
    path('<int:candidate_id>', get_candidate_info, name='candidate_profile')
]
