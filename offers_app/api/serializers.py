from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from django.db.models import Min
from django.conf import settings
from .functions import *

class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']



class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)  
    user = serializers.ReadOnlyField(source='user.user.id')
    min_price = serializers.ReadOnlyField()
    min_delivery_time = serializers.ReadOnlyField()
    image = serializers.ImageField(required=False, allow_null=True)

    def get_image(self, obj):
        '''
        Get the image URL.
        '''
        if obj.image:
            return f"{settings.MEDIA_URL}{obj.image.name}"  
        return None 

    class Meta:
        model = Offer
        fields = '__all__'



    def create(self, validated_data):
        '''
        Create and return a new offer.
        '''
        validated_data.pop('user', None)
        details_data = validated_data.pop('details', [])
        user = self.context['request'].user.userprofile

        offer = Offer.objects.create(user=user, **validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)

        offer.min_price = offer.details.aggregate(Min('price'))['price__min']
        offer.min_delivery_time = offer.details.aggregate(Min('delivery_time_in_days'))['delivery_time_in_days__min']
        offer.save()

        return offer


    def update(self, instance, validated_data):
        '''
        Update and return an existing offer.
        '''
        details_data = validated_data.pop('details', None)
        
        update_offer(instance, validated_data)

        update_offer_details(instance, details_data)

        return instance
