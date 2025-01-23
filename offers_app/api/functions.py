from offers_app.models import OfferDetail, Offer
from django.db.models import Min
from decimal import Decimal
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied


def update_offer(instance, validated_data):
    """
    Actualize the offer.
    """
    instance.title = validated_data.get('title', instance.title)
    instance.description = validated_data.get('description', instance.description)
    instance.image = validated_data.get('image', instance.image if instance.image != "" else "")
    instance.save()

def update_offer_details(instance, details_data):
    """
    Actualize the offer details.
    """
    if details_data is not None:
        instance.details.all().delete()
        for detail_data in details_data:
            OfferDetail.objects.create(offer=instance, **detail_data)
        
        instance.min_price = instance.details.aggregate(Min('price'))['price__min']
        instance.min_delivery_time = instance.details.aggregate(Min('delivery_time_in_days'))['delivery_time_in_days__min']
        instance.save()

def check_user_permissions(user):
    '''
    Check if the user has the right permissions to create an offer.
    '''
    if not user.is_authenticated:
        raise PermissionDenied(detail="Authentication required to create an offer.")
    if not hasattr(user, 'userprofile') or user.userprofile.type != 'business':
        raise PermissionDenied(detail="Only business users are allowed to create offers.")

def process_image(validated_data):
    '''
    Process the image.
    '''
    image = validated_data.pop('image', None)
    if image is None:
        validated_data['image'] = ""
    return validated_data

def create_offer_and_details(user_profile, validated_data, details_data):
    '''
    Create and return a new offer.
    '''
    offer = Offer.objects.create(user=user_profile, **validated_data)
    for detail_data in details_data:
        OfferDetail.objects.create(offer=offer, **detail_data)
    offer.min_price = offer.details.aggregate(Min('price'))['price__min']
    offer.min_delivery_time = offer.details.aggregate(Min('delivery_time_in_days'))['delivery_time_in_days__min']
    offer.save()
    return offer

