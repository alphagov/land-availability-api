from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnlyUser(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user is not None
        else:
            return request.user.is_staff
