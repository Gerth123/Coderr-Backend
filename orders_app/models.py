from django.db import models
from users_auth_app.models import UserProfile
from django.contrib.auth.models import User
from offers_app.models import OfferDetail

class Order(models.Model):
    OFFER_TYPES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    offer_detail = models.ForeignKey(OfferDetail, on_delete=models.CASCADE, related_name='orders', blank=True, null=True)
    customer_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='customer_orders', blank=True, null=True)
    business_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='business_offers', blank=True, null=True)
    title = models.CharField(max_length=255, blank=True)
    revisions = models.IntegerField(default=0, blank=True, null=True)
    delivery_time_in_days = models.PositiveIntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    features = models.JSONField(blank=True, null=True)
    offer_type = models.CharField(max_length=10, choices=OFFER_TYPES, default='basic', blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.offer_type}) - {self.status}"
