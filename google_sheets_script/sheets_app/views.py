from django.shortcuts import render

from .models import Orders


def index(request):
    """View function for processing the main page of the site"""
    orders = Orders.objects.all()

    context = {
        'orderlines': orders,
        }
    return render(request, 'sheets_app/index.html', context)
