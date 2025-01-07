from django.contrib import admin

from users_auth_app.models import UserProfile
from offers_app.models import Offer
from orders_app.models import Order

admin.site.register(UserProfile)
admin.site.register(Offer)
admin.site.register(Order)

