from django.urls import path

from .views import OrderListCreateView, OrderListDetailView


urlpatterns = [
    path('', OrderListCreateView.as_view(), name='orders-list'),
    path('<int:pk>/', OrderListDetailView.as_view(), name='order-detail'),
]