from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from candidates.forms import CandidateForm
from candidates.models import Candidate


def get_all_candidates(request: HttpRequest) -> HttpResponse:
    template_dict = {'header': 'Candidates list',
                     'candidates': Candidate.objects.filter(is_active=True, is_staff=False)}
    return render(request, 'candidates/main_page.html', context=template_dict)


def get_candidate_info(request: HttpRequest, candidate_id: int) -> HttpResponse:
    template_dict = {'header': 'Candidate profile',
                     'candidate': Candidate.objects.get(id=candidate_id)}
    return render(request, 'candidates/candidate_info.html', context=template_dict)


def edit_candidate(request: HttpRequest, candidate_id: int) -> HttpResponse:
    candidate_obj = get_object_or_404(Candidate, pk=candidate_id)
    form = CandidateForm(instance=candidate_obj)
    if request.method == 'POST':
        form = CandidateForm(request.POST, instance=candidate_obj)
        if form.is_valid():
            return form.save() and redirect(candidate_obj.get_absolute_url())

    return render(request, 'candidates/edit_candidate.html',
                  context={'header': 'Edit candidate', 'form': form})
