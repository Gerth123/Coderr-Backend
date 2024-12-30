from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    file = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    working_hours = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=10, choices=[('business', 'Business'), ('personal', 'Personal')])
    email = models.EmailField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        
        if not self.slug:
            self.slug = slugify(self.user.username)

        super(UserProfile, self).save(*args, **kwargs)
