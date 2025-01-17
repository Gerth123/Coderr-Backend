from rest_framework import generics
from users_auth_app.models import UserProfile
from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from .functions import *

class UserProfileList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer   

class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = UserProfile.objects.all()

    def get_serializer_class(self):
        '''
        Set the serializer class based on the request method.
        '''
        if self.request.method == 'GET':
            return UserProfileSerializer
        if self.request.method == 'PATCH':
            return UserProfilePatchSerializer  
        return UserProfileSerializer  

    def get_object(self):
        '''
        Get the object to be modified.
        '''
        obj = get_object_or_404(UserProfile, pk=self.kwargs.get('pk'))
        
        if self.request.method == 'GET':
            return obj
        
        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied("You do not have permission to modify this profile.")
        
        return obj

    def perform_update(self, serializer):
        '''
        Update the object.
        '''
        serializer.save(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        '''
        Patch the relevant dates of the object.
        '''
        partial = kwargs.pop('partial', True) 
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BusinessProfileList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = UserProfile.objects.filter(type='business')
    serializer_class = SpecificUserProfileSerializer

    def get_queryset(self):
        '''
        Get the business profiles.
        '''
        return UserProfile.objects.filter(type='business')

class BusinessProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = UserProfile.objects.filter(type='business')
    serializer_class = SpecificUserProfileSerializer

    def get_object(self):
        '''
        Get the business profile detail.
        '''
        obj = get_object_or_404(UserProfile, pk=self.kwargs.get('pk'), type='business')
        if obj.user != self.request.user and not self.request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return obj

class CustomerProfileList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = UserProfile.objects.filter(type='customer')
    serializer_class = SpecificUserProfileSerializer

    def get_queryset(self):
        '''
        Get the customer profiles.
        '''
        return UserProfile.objects.filter(type='customer')

class CustomerProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = UserProfile.objects.filter(type='customer')
    serializer_class = SpecificUserProfileSerializer

    def get_object(self):
        '''
        Get the customer profile detail.
        '''
        obj = get_object_or_404(UserProfile, pk=self.kwargs.get('pk'), type='customer')
        if obj.user != self.request.user and not self.request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return obj

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        '''
        Register a new user.
        '''
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token': token.key,
                'username': saved_account.username,
                'email': saved_account.email,
                'user_id': saved_account.id
            }
            return Response(data, status.HTTP_200_OK) 
        else:
            data = serializer.errors
            return Response(data, status.HTTP_400_BAD_REQUEST) 


class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Main entry point for login logic.
        """
        token = request.data.get('token')
        if token:
            user = validate_token(token)
            if user:
                token_obj = Token.objects.get(user=user)
                return generate_response(user, token_obj)
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        return handle_username_login(request.data)


