from django.shortcuts import render

from .models import Orders


def index(request):
    """Вью-функция для обработки главной страницы сайта"""
    orders = Orders.objects.all()

    context = {
        'orderlines': orders,
        }
    return render(request, 'sheets_app/index.html', context)
