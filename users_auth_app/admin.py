from django.contrib import admin

from users_auth_app.models import UserProfile
from offers_app.models import Offer

admin.site.register(UserProfile)
admin.site.register(Offer)
