from rest_framework.permissions import BasePermission
from users_auth_app.models import UserProfile

class IsCustomerUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False        
        if request.user.is_staff or request.user.is_superuser:
            return True
        try:
            customer_profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            return False          
        return customer_profile.type == 'customer'
