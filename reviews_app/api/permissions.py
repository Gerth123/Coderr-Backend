from rest_framework import permissions

class IsReviewerOrAdmin(permissions.BasePermission):
    """
    Custom permission: Allow anyone to read, but only the reviewer or admin to update or delete.
    """
    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, OPTIONS for all users
        if request.method in permissions.SAFE_METHODS:  # SAFE_METHODS includes GET, HEAD, OPTIONS
            return True

        # Allow only reviewer or admin to modify
        return obj.reviewer == request.user or request.user.is_staff
