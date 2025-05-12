from rest_framework import permissions

class AdminOrReadOnlyPermission(permissions.IsAdminUser):
    """
    Custom permission to only allow admins to edit objects.
    """
    def has_permission(self, request, view):
        # Allow read-only access for non-authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow full access for admin users
        else:
            return bool(request.user and request.user.is_staff)
        

class ReviewUserReadOnlypermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.apiuser == request.user