from rest_framework import serializers
from orders_app.models import Order
from offers_app.models import OfferDetail
from users_auth_app.models import UserProfile
from rest_framework.response import Response
from rest_framework import status
from .functions import *

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
            'offer_type', 'created_at', 'updated_at'
        ]

    def get_revisions(self, obj):
        '''
        Get the revisions.
        '''
        if obj.revisions == -1:
            return "Unbegrenzte"
        if obj.revisions == 0 or None:
            return "Keine"
        return obj.revisions
    

    def create(self, validated_data):
        '''
        Create and return a new order.
        '''
        offer_detail = validated_data.get('offer_detail')
        business_user = offer_detail.offer.user
        customer_user = getattr(self.context['request'].user, 'userprofile', None)
        if not customer_user:
            raise ValueError("Der Benutzer hat kein UserProfile.")

        order = create_order(offer_detail, customer_user)

        return order
