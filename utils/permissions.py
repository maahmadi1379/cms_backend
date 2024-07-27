from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Custom permission class to only allow access if the current user is both staff and a superuser.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.is_staff and request.user.is_superuser


class IsEmployee(BasePermission):
    """
    Custom permission class to only allow access if the current user is a staff and is not a superuser.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.is_staff and (not request.user.is_superuser)


class IsStudent(BasePermission):
    """
    Custom permission class to only allow access if the current user is not both staff and a superuser.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return (not request.user.is_staff) and (not request.user.is_superuser)
