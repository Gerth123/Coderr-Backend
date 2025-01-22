from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from django.db.models import Min
from django.conf import settings
from .functions import *
from users_auth_app.models import UserProfile
from rest_framework.exceptions import PermissionDenied
from decimal import Decimal

class OfferDetailSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

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
    image = serializers.SerializerMethodField()
    user_details = UserProfileSerializer(source='user', read_only=True)

    def get_image(self, obj):
        '''
        Get the image URL.
        '''
        if obj.image and obj.image != "":
            return f"{settings.MEDIA_URL}{obj.image.name}"  
        return ""

    class Meta:
        model = Offer
        fields = '__all__'

    def create(self, validated_data):
        """
        Create and return a new offer.
        """
        user = self.context['request'].user
        if not user.is_authenticated:
            raise PermissionDenied(detail="Authentication required to create an offer.")

        if not hasattr(user, 'userprofile') or user.userprofile.type != 'business':
            raise PermissionDenied(detail="Only business users are allowed to create offers.")

        validated_data.pop('user', None)
        image = validated_data.pop('image', None)
        if image is None:
            validated_data['image'] = ""
        details_data = validated_data.pop('details', [])
        user_profile = user.userprofile

        offer = Offer.objects.create(user=user_profile, **validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        print(offer)
        offer.min_price = offer.details.aggregate(Min('price'))['price__min']
        offer.min_delivery_time = offer.details.aggregate(Min('delivery_time_in_days'))['delivery_time_in_days__min']
        offer.save()

        return offer


    def update(self, instance, validated_data):
        '''
        Update and return an existing offer.
        '''
        details_data = validated_data.pop('details', None)

        image = validated_data.pop('image', None)
        if image is None:
            validated_data['image'] = ""
        
        update_offer(instance, validated_data)

        update_offer_details(instance, details_data)

        return instance
