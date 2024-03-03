from django.http import Http404, HttpRequest, HttpResponse


def show_custom_404(request: HttpRequest, exception: Http404) -> HttpResponse:
    return HttpResponse('<h1>Страница не найдена</h1>')
