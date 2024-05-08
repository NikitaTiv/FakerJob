from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect


def show_custom_404(request: HttpRequest, exception: Http404) -> HttpResponse:
    return HttpResponse('<h1>Страница не найдена</h1>')


def main_redirect(request: HttpRequest) -> HttpResponse:
    return redirect('candidate_list', permanent=True)
