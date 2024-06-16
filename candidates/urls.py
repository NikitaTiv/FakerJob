from django.urls import path

from candidates.views import CandidateEdit, CandidateInfo, CandidateList


urlpatterns = [
    path('', CandidateList.as_view(), name='candidate_list'),
    path('<int:candidate_id>', CandidateInfo.as_view(), name='candidate_profile'),
    path('<int:candidate_id>/edit', CandidateEdit.as_view(), name='edit_candidate')
]
