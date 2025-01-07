from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from django.db.models import Min
from django.conf import settings

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
        if obj.image:
            return f"{settings.MEDIA_URL}{obj.image.name}"  
        return None 

    class Meta:
        model = Offer
        fields = '__all__'



    def create(self, validated_data):
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
        details_data = validated_data.pop('details', None)  
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.save()

        if details_data is not None:
            instance.details.all().delete()  
            for detail_data in details_data:
                OfferDetail.objects.create(offer=instance, **detail_data) 

        instance.min_price = instance.details.aggregate(Min('price'))['price__min']
        instance.min_delivery_time = instance.details.aggregate(Min('delivery_time_in_days'))['delivery_time_in_days__min']
        instance.save()

        return instance
