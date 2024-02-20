from django.http import HttpResponse


def show_custom_404(request, exception):
    return HttpResponse('<h1>Страница не найдена</h1>')
