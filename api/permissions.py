from rest_framework import permissions


class IsAuthorAdminModeratorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'POST':
            return bool(request.user and request.user.is_authenticated)

        return bool(
            request.user and (
                request.user == obj.author or
                request.user.is_moderator or
                request.user.is_admin
            )
        )


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            return request.user.is_admin
<<<<<<< HEAD

        return False
=======
>>>>>>> 2662c4ff4a4f7bc0970d196f3bba2240f47da26f


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin

        return False
