from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from django.db.models import Min

class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)  
    min_price = serializers.ReadOnlyField()
    min_delivery_time = serializers.ReadOnlyField()

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time']

    def create(self, validated_data):
        details_data = validated_data.pop('details')  # Details aus den Validierungsdaten extrahieren

        # Erstelle das Offer-Objekt und speichere es, damit eine ID generiert wird
        offer = Offer.objects.create(**validated_data)

        # Jetzt, da das Offer-Objekt gespeichert ist und eine ID hat, erstellen wir die OfferDetail-Objekte
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)

        # Berechne min_price und min_delivery_time nach der Erstellung des Offer-Objekts
        offer.min_price = offer.details.aggregate(Min('price'))['price__min']
        offer.min_delivery_time = offer.details.aggregate(Min('delivery_time_in_days'))['delivery_time_in_days__min']
        offer.save()  # Speichere das Offer-Objekt nach der Berechnung von min_price und min_delivery_time

        return offer

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)  # Details-Daten extrahieren

        # Aktualisiere die Felder des bestehenden Offer-Objekts
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        # Lösche alte Details und erstelle neue, wenn Details-Daten übermittelt wurden
        if details_data is not None:
            instance.details.all().delete()  # Lösche alte Details
            for detail_data in details_data:
                OfferDetail.objects.create(offer=instance, **detail_data)  # Erstelle neue Details

        # Berechne min_price und min_delivery_time nach der Aktualisierung
        instance.min_price = instance.details.aggregate(Min('price'))['price__min']
        instance.min_delivery_time = instance.details.aggregate(Min('delivery_time_in_days'))['delivery_time_in_days__min']
        instance.save()

        return instance
