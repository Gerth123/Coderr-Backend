from django.db import models
from django.db.models import Min
from users_auth_app.models import UserProfile
from django import forms
from django.core.exceptions import ValidationError

class Offer(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="offers", 
    )
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="offers/images/", null=False, blank=True, default="")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_delivery_time = models.IntegerField(null=True, blank=True)

    def __str__(self):
        '''
        Returns a string representation of the model.
        '''
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
        related_name="details", 
    )
    title = models.CharField(max_length=255)
    revisions = models.IntegerField(default=0)
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()
    offer_type = models.CharField(max_length=10, choices=OFFER_TYPES)

    def __str__(self):
        '''
        Returns a string representation of the model.
        '''
        return f"{self.title} - {self.offer_type}"

    def clean(self):
        '''
        Custom validation for the model.
        '''
        if self.revisions < -1:
            raise ValidationError("Revisions müssen -1 oder größer sein.")

        if self.delivery_time_in_days <= 0:
            raise ValidationError("delivery_time_in_days muss positiv sein.")

        if not self.features or not isinstance(self.features, list) or len(self.features) < 1:
            raise ValidationError("Es muss mindestens ein Feature vorhanden sein.")

        super().clean()