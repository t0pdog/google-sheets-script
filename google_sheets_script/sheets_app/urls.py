from django.urls import path

from . import views


app_name = 'sheets_app'

urlpatterns = [
    path('', views.index, name='index'),
]