from rest_framework.permissions import BasePermission

class IsBusinessOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        '''
        Check if the user is a business owner.
        '''
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        return request.user.is_authenticated and hasattr(request.user, 'userprofile') and request.user.userprofile.type == 'business'

    def has_object_permission(self, request, view, obj):
        '''
        Check if the user is the owner of the business.
        '''
        if request.method in ['PATCH', 'DELETE']:
            return obj.user == request.user.userprofile
        return True
