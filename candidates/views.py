from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from candidates.models import Candidate


def get_all_candidates(request: HttpRequest) -> HttpResponse:
    template_dict = {'header': 'Candidates list', 'candidates': Candidate.objects.filter(is_active=True)}
    return render(request, 'candidates/main_page.html', context=template_dict)


def get_candidate_info(request: HttpRequest, candidate_id: int) -> HttpResponse:
    return HttpResponse(f'<h1>Страница о кандидате с id {candidate_id}')
