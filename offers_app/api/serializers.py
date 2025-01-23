from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from django.db.models import Min
from django.conf import settings
from .functions import *
from users_auth_app.models import UserProfile
from rest_framework.exceptions import PermissionDenied
from decimal import Decimal

class CustomFloatField(serializers.FloatField):
    def to_representation(self, value):
        return float(f"{value:.2f}")

class OfferDetailSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    price = CustomFloatField()
    # price = serializers.SerializerMethodField()
    # price = MoneyField(max_digits=15, decimal_places=2, default_currency='EUR')

    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'url']

    def get_url(self, obj):
        '''
        Get the URL of the offer detail.
        '''
        return f"/offerdetails/{obj.id}/"
        

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile.
    """
    first_name = serializers.CharField(source='user.userprofile.first_name')
    last_name = serializers.CharField(source='user.userprofile.last_name')
    username = serializers.CharField(source='user.username')

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'username']


class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)  
    user = serializers.ReadOnlyField(source='user.user.id')
    min_price = serializers.ReadOnlyField()
    min_delivery_time = serializers.ReadOnlyField()
    image = serializers.ImageField(required=False, allow_null=True)
    user_details = UserProfileSerializer(source='user', read_only=True)

    class Meta:
        model = Offer
        fields = '__all__'

    def create(self, validated_data):
        """
        Create and return a new offer.
        """
        user = self.context['request'].user

        check_user_permissions(user)
        validated_data.pop('user', None)
        validated_data = process_image(validated_data)
        
        details_data = validated_data.pop('details', [])
        user_profile = user.userprofile

        offer = create_offer_and_details(user_profile, validated_data, details_data)

        return offer


    def update(self, instance, validated_data):
        '''
        Update and return an existing offer.
        '''
        details_data = validated_data.pop('details', None)
        
        update_offer(instance, validated_data)

        update_offer_details(instance, details_data)

        return instance
