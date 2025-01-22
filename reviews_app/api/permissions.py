from rest_framework import permissions

class IsReviewerOrAdmin(permissions.BasePermission):
    """
    Custom permission: Allow anyone to read, but only the reviewer or admin to update or delete.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.reviewer == request.user or request.user.is_staff
