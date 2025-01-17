from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    business_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews_received'
    )
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews_given'
    )
    rating = models.PositiveSmallIntegerField(default=1)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at'] 

    def __str__(self):
        '''
        Returns a string representation of the model.
        '''
        return f"Review by {self.reviewer.username} for {self.business_user.username}: {self.rating}/5"
