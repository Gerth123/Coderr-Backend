from django.contrib import admin

from users_auth_app.models import UserProfile
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order
from reviews_app.models import Review

admin.site.register(UserProfile)
admin.site.register(Offer)
admin.site.register(OfferDetail)
admin.site.register(Order)
admin.site.register(Review)


