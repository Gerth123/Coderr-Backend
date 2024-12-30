from django.urls import path

from .views import offers_list

urlpatterns = [
    path('', offers_list, name='offers-list'),
]