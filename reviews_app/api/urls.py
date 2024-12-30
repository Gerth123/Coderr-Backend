from django.urls import path

from .views import reviews_list

urlpatterns = [
    path('', reviews_list, name='reviews-list'),
]