from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from candidates.models import Candidate


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse('привет')


def profile(request: HttpRequest) -> HttpResponse:
    template_dict = {'header': 'Страница о кандидате', 'candidate': Candidate.objects.first().__dict__}
    return render(request, 'candidates/main_page.html', context=template_dict)
