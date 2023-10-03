from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Редактирование только для администратора"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsOwner(permissions.BasePermission):
    """Доступ к объекту для владельца объекта"""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user and request.user.is_authenticated
