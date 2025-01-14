from rest_framework import generics
from orders_app.models import Order
from .serializers import OrderSerializer
from rest_framework import permissions
from .permissions import IsCustomerUser
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

        if user_profile.type == 'personal':
            return Order.objects.filter(customer_user=user_profile).exclude(customer_user__isnull=True)
        
        return Order.objects.none()


    def perform_create(self, serializer):
        user_profile = UserProfile.objects.get(user=self.request.user)
        serializer.save(customer_user=user_profile)

class OrderListDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomerUser, permissions.IsAdminUser]
    queryset = Order.objects.all()

    def get_object(self):
        obj = get_object_or_404(Order, pk=self.kwargs.get('pk'))

        if obj.customer_user != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied("You do not have permission to access this order.")

        return obj
    
    def perform_destroy(self, instance):
        if not self.request.user.is_superuser:
            raise PermissionDenied("Only admins can delete orders.")

        instance.delete()

class OpenOrdersCountView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()

    def get(self, request, *args, **kwargs):
        # Extrahiere den business_user_id aus den URL-Parametern (nicht query_params)
        business_user_id = kwargs.get('business_user_id')  # Der pk aus der URL (/api/order-count/<int:pk>/)

        # Überprüfe, ob business_user_id vorhanden ist
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
            # Allgemeine Fehlerbehandlung, falls etwas anderes schief geht
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
            # Allgemeine Fehlerbehandlung, falls etwas anderes schief geht
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








