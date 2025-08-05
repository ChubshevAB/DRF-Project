from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name="moderators").exists()


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.owner == request.user
            or request.user.groups.filter(name="moderators").exists()
        )


class IsOwnerOrModeratorForList(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name="moderators").exists():
            return True
        return view.action != "list"  # Для списка проверяем в queryset
