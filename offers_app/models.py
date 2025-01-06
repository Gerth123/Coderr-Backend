from django.db import models
from django.db.models import Min
from users_auth_app.models import UserProfile
from django import forms

class Offer(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="offers"
    )
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="offers/images/", null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_delivery_time = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title


class OfferDetail(models.Model):
    OFFER_TYPES = [
        ("basic", "Basic"),
        ("standard", "Standard"),
        ("premium", "Premium")
    ]

    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name="details"
    )
    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()
    offer_type = models.CharField(max_length=10, choices=OFFER_TYPES)

    def __str__(self):
        return f"{self.title} - {self.offer_type}"
