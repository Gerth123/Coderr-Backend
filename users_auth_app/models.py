from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100, blank=True,  default='', null=True)
    last_name = models.CharField(max_length=100, blank=True,  default='', null=True)
    file = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    location = models.CharField(max_length=255,  default='', blank=True, null=True)
    tel = models.CharField(max_length=20,  default='', blank=True, null=True)
    description = models.TextField(  default='',blank=True, null=True)
    working_hours = models.CharField(max_length=50,  default='', blank=True, null=True)
    type = models.CharField(max_length=10, choices=[('business', 'Business'), ('customer', 'Customer')], default='customer')
    email = models.EmailField(blank=False,  default='', null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        '''
        Returns a string representation of the model.
        '''
        return self.user.username

    def save(self, *args, **kwargs):
        '''
        Override the save method to set the slug field.
        '''
        if self.email:
            self.email = self.email.lower()
        
        if not self.slug:
            self.slug = slugify(self.user.username)

        super(UserProfile, self).save(*args, **kwargs)
