from rest_framework import generics
from orders_app.models import Order
from offers_app.models import OfferDetail
from .serializers import OrderSerializer
from rest_framework import permissions
from django.db import models
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsCustomerUser



class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsCustomerUser, ]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(
            models.Q(customer_user=user) | models.Q(business_user=user)
        )
    
    def perform_create(self, serializer):
        serializer.save(customer_user=self.request.user)