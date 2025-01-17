from rest_framework import generics
from orders_app.models import Order
from .serializers import OrderSerializer
from rest_framework import permissions
from users_auth_app.models import UserProfile
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from .functions import *



class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        '''
        Get the orders for the current user.
        '''
        user = self.request.user
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return Order.objects.none()
        if user_profile.type == 'business':
            return Order.objects.filter(business_user=user_profile).exclude(business_user__isnull=True)
        if user_profile.type == 'customer':
            return Order.objects.filter(customer_user=user_profile).exclude(customer_user__isnull=True)
        return Order.objects.none()

    def perform_create(self, serializer):
        '''
        Create a new order.
        '''
        try:
            user_profile = UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            raise PermissionDenied("User profile not found.")
        if user_profile.type != 'customer':
            raise PermissionDenied("Only customers can create orders.")
        
        serializer.save(customer_user=user_profile)

class OrderListDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()

    def get_object(self):
        '''
        Get the order detail.
        '''
        obj = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        if (
            obj.customer_user.user.id != self.request.user.id
            and obj.business_user.user.id != self.request.user.id
            and not self.request.user.is_superuser
        ):
            raise PermissionDenied("You do not have permission to access this order.")

        return obj
    
    def perform_destroy(self, instance):
        '''
        Delete the order.
        '''
        if not self.request.user.is_superuser:
            raise PermissionDenied("Only admins can delete orders.")

        instance.delete()

    def partial_update(self, request, *args, **kwargs):
        '''
        Update the order.
        '''
        instance = self.get_object()
        if (
            self.request.user.id != instance.business_user.user.id and
            not self.request.user.is_superuser
        ):
            raise PermissionDenied("Only the business user or admins can update the order.")
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

class OpenOrdersCountView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''
        Get the count of open orders for a business user.
        '''
        business_user_id = kwargs.get('business_user_id')
        if not business_user_id:
            return Response({'error': 'business_user_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        business_user = get_business_user(business_user_id)
        if not business_user:
            return Response({'error': 'Business user not found'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            count = count_orders('in_progress', business_user_id)
            return Response({'order_count': count}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CompletedOrdersCountView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''
        Get the count of completed orders for a business user.
        '''
        business_user_id = kwargs.get('business_user_id')
        if not business_user_id:
            return Response({'error': 'business_user_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        business_user = get_business_user(business_user_id)
        if not business_user:
            return Response({'error': 'Business user not found'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            count = count_orders('completed', business_user_id)
            return Response({'completed_order_count': count}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








