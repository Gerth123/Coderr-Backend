from offers_app.models import OfferDetail
from django.db.models import Min

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
