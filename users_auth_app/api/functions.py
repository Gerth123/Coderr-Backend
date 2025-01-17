from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UsernameAuthTokenSerializer

def validate_token(token):
    """
    Validates the token and returns the user if valid.
    """
    try:
        token_obj = Token.objects.get(key=token)
        return token_obj.user
    except Token.DoesNotExist:
        return None

def generate_response(user, token):
    """
    Generates a response with user details and token.
    """
    return Response({
        'token': token.key,
        'username': user.username,
        'email': user.email,
        'user_id': user.id
    }, status=status.HTTP_200_OK)

def handle_username_login(data):
    """
    Handles login via username and password.
    """
    serializer = UsernameAuthTokenSerializer(data=data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return generate_response(user, token)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
