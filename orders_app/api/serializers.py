from rest_framework import serializers
from orders_app.models import Order
from offers_app.models import OfferDetail
from users_auth_app.models import UserProfile

class OrderSerializer(serializers.ModelSerializer):
    customer_user = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(), required=False)
    business_user = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(), required=False)
    offer_detail_id = serializers.PrimaryKeyRelatedField(queryset=OfferDetail.objects.all(), source='offer_detail')
    revisions = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer_user', 'offer_detail_id', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at']
        read_only_fields = [
            'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 
            'offer_type', 'status', 'created_at', 'updated_at'
        ]

    def get_revisions(self, obj):
        if obj.revisions == -1:
            return "Unbegrenzte"
        if obj.revisions == 0 or None:
            return "Keine"
        return obj.revisions
    

    def create(self, validated_data):
        offer_detail = validated_data.get('offer_detail')
        business_user = offer_detail.offer.user
        customer_user = getattr(self.context['request'].user, 'userprofile', None)
        if not customer_user:
            raise ValueError("Der Benutzer hat kein UserProfile.")

        order = Order.objects.create(
            customer_user=customer_user,
            business_user=business_user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            status='in_progress'  
        )

        return order
