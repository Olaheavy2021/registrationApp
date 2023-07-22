from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    # Allow GET requests for anyone
    # but allow only admin users for other actions
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsOwnerOrAdmin(permissions.BasePermission):
    # Allow admin or currently logged in user to edit their own resource
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user
