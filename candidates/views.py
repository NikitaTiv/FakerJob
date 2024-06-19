from typing import Any

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, FormView

from candidates.forms import CandidateForm
from candidates.mixins import HeaderMixin
from candidates.models import Candidate


class CandidateList(HeaderMixin, ListView):
    queryset = Candidate.objects.filter(is_active=True, is_staff=False)
    template_name = 'candidates/main_page.html'
    header_name = 'Candidates list'


class CandidateInfo(HeaderMixin, DetailView):
    queryset = Candidate.objects.filter(is_active=True, is_staff=False)
    template_name = 'candidates/candidate_info.html'
    pk_url_kwarg = 'candidate_id'
    header_name = 'Candidate profile'


class CandidateEdit(HeaderMixin, FormView):
    form_class = CandidateForm
    template_name = 'candidates/edit_candidate.html'
    header_name = 'Edit candidate'

    def setup(self, request: WSGIRequest, *args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        super().setup(request, *args, **kwargs)
        self.candidate_obj = get_object_or_404(Candidate, pk=self.kwargs.get('candidate_id'))

    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs.update({'instance': self.candidate_obj})

        return kwargs

    def form_valid(self, form: CandidateForm) -> HttpResponseRedirect:
        return form.save() and HttpResponseRedirect(reverse('candidate_profile',
                                                            kwargs={'candidate_id': self.candidate_obj.id}))

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, str | Candidate]:
        context_data = super().get_context_data(**kwargs)
        context_data.update({'candidate': self.candidate_obj})
        return context_data
