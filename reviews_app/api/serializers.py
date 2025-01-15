from rest_framework import serializers
from reviews_app.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'reviewer']

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            business_user = data.get('business_user')
            reviewer = request.user

            if not business_user:
                raise serializers.ValidationError({"business_user": "This field is required."})

            if Review.objects.filter(business_user=business_user, reviewer=reviewer).exists():
                raise serializers.ValidationError("You can only leave one review per business.")
        return data

    def create(self, validated_data):
        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)

