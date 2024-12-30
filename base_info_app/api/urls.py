from django.urls import path

from .views import base_info_list

urlpatterns = [
    path('', base_info_list, name='base-info-list'),
]