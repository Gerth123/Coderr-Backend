from rest_framework.decorators import api_view
from rest_framework.response import Response
from reviews_app.models import Review
from users_auth_app.models import UserProfile
from offers_app.models import Offer
from django.db.models import Avg

@api_view(['GET'])
def base_info_list(request):
    review_count = Review.objects.count()
    average_rating = Review.objects.aggregate(average_rating=Avg('rating'))['average_rating'] or 0
    business_profile_count = UserProfile.objects.filter(type='business').count()
    offer_count = Offer.objects.count()

    data = {
        "review_count": review_count,
        "average_rating": round(average_rating, 1),
        "business_profile_count": business_profile_count,
        "offer_count": offer_count,
    }
    return Response(data)