from rest_framework import generics
from orders_app.models import Order
from .serializers import OrderSerializer
from rest_framework import permissions
from users_auth_app.models import UserProfile
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status



class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
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
        obj = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        if (
            obj.customer_user.user.id != self.request.user.id
            and obj.business_user.user.id != self.request.user.id
            and not self.request.user.is_superuser
        ):
            raise PermissionDenied("You do not have permission to access this order.")

        return obj
    
    def perform_destroy(self, instance):
        if not self.request.user.is_superuser:
            raise PermissionDenied("Only admins can delete orders.")

        instance.delete()

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        if self.request.user.is_superuser and self.request.user.id != instance.customer_user.user.id:
            raise PermissionDenied("Only the creator of the order can update it.")

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

class OpenOrdersCountView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()

    def get(self, request, *args, **kwargs):
        business_user_id = kwargs.get('business_user_id') 
        if not business_user_id:
            return Response({'error': 'business_user_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            business_user = UserProfile.objects.get(pk=business_user_id)
            if business_user.type != 'business':
                return Response({'error': 'Business user not found'}, status=status.HTTP_400_BAD_REQUEST)
            
            count = Order.objects.filter(
                status='in_progress',
                business_user_id=business_user_id
            ).count()

            return Response({'order_count': count}, status=status.HTTP_200_OK)

        except UserProfile.DoesNotExist:
            return Response({'error': 'Business user not found'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CompletedOrdersCountView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()

    def get(self, request, *args, **kwargs):
        business_user_id = kwargs.get('business_user_id') 

        if not business_user_id:
            return Response({'error': 'business_user_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            business_user = UserProfile.objects.get(pk=business_user_id)

            if business_user.type != 'business':
                return Response({'error': 'Business user not found'}, status=status.HTTP_400_BAD_REQUEST)

            count = Order.objects.filter(
                status='completed',
                business_user_id=business_user_id
            ).count()

            return Response({'completed_order_count': count}, status=status.HTTP_200_OK)

        except UserProfile.DoesNotExist:
            return Response({'error': 'Business user not found'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








