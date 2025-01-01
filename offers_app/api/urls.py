from django.urls import path

from .views import OfferListCreateView, SingleOfferView

urlpatterns = [
    # path('', OfferListAPIView.as_view(), name='offers-list'),
    path('', OfferListCreateView.as_view(), name='offers-create'),
    path('<int:pk>/', SingleOfferView.as_view(), name='single-offer'),
]