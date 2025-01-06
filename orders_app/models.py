from django.db import models
from django.contrib.auth.models import User

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

    customer_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_offers')
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_offers')
    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()  # Requires PostgreSQL for JSONField or Django 3.1+
    offer_type = models.CharField(max_length=10, choices=OFFER_TYPES, default='basic')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.offer_type}) - {self.status}"