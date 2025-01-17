from users_auth_app.models import UserProfile
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from utils.validators import validate_no_html
from django.conf import settings


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    file = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source='user.id')

    def get_file(self, obj):
        '''
        Get the file URL.
        '''
        if obj.file:
            return f"{settings.MEDIA_URL}{obj.file.name}"  
        return None 

    class Meta:
        model = UserProfile
        fields = '__all__'

class UserProfilePatchSerializer(serializers.ModelSerializer):
    file = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = UserProfile
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(
        max_length=100, validators=[validate_no_html])
    email = serializers.CharField(
        max_length=100, validators=[validate_no_html])

    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'email']


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=[('business', 'Business'), ('customer', 'Customer')], default='customer')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'type']

    def validate_username(self, value):
        """
        Check if the username is already in use.
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Der Benutzername ist bereits vergeben.")
        return value

    def validate_email(self, value):
        """
        Check if the email is already in use.
        """
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError(
                "Die E-Mail-Adresse ist bereits registriert.")
        return value

    def save(self):
        '''
        Create and return a new user account.
        '''
        user = self.create_user()
        user_profile = self.create_user_profile(user)
        return user

    def create_user(self):
        '''
        Create and return a new user account.
        '''
        password = self.validated_data['password']
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'].lower(),
        )
        user.set_password(password)
        user.save()
        return user

    def create_user_profile(self, user):
        '''
        Create and return a new user profile.
        '''
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        user_profile.type = self.validated_data.get('type', user_profile.type)
        user_profile.email = self.validated_data.get('email', user_profile.email)
        user_profile.save()

        return user_profile

class UsernameAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        '''
        Validate the username and password.
        '''
        username = attrs.get('username')
        password = attrs.get('password')
        if username and password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise serializers.ValidationError("Benutzer mit diesem Benutzernamen existiert nicht.")
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Ungültige Anmeldedaten.")
        else:
            raise serializers.ValidationError("Benutzername und Passwort sind erforderlich.")
        attrs['user'] = user
        return attrs
    
class SpecificUserProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()
    uploaded_at = serializers.SerializerMethodField()
    type = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['user', 'file', 'uploaded_at', 'type']

    def get_user(self, obj):
        '''
        Get the user details.
        '''
        return {            
            'pk': obj.user.id,
            'username': obj.user.username,
            'first_name': obj.user.userprofile.first_name,
            'last_name': obj.user.userprofile.last_name,
            'file': self.get_file(obj),
        }
    
    def get_file(self, obj):
        '''
        Get the file URL.
        '''
        if obj.file:
            return f"{settings.MEDIA_URL}{obj.file.name}"  
        return None
    
    def get_uploaded_at(self, obj):
        '''
        Get the uploaded at date.    
        '''
        return obj.user.userprofile.created_at
