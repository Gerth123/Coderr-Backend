from users_auth_app.models import UserProfile
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from utils.validators import validate_no_html


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

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
    type = serializers.ChoiceField(choices=[('business', 'Business'), ('personal', 'Personal')])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'type']

    def validate_username(self, value):
        """
        Überprüft, ob der Benutzername bereits existiert.
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Der Benutzername ist bereits vergeben.")
        return value

    def validate_email(self, value):
        """
        Überprüft, ob die E-Mail-Adresse bereits existiert.
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
                raise serializers.ValidationError(
                    "Benutzer mit diesem Benutzernamen existiert nicht.")

            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Ungültige Anmeldedaten.")
        else:
            raise serializers.ValidationError(
                "Benutzername und Passwort sind erforderlich.")

        attrs['user'] = user
        return attrs
