from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_superuser


class IsWebsiteOwnerorAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        # if request.method in SAFE_METHODS:
        #    return True
        return obj.user == request.user

# class IsShopOwnerorAdminorReadOnly(permissions.BasePermission):
#     def has_permission(self, request, view, obj):
#         if request.users in obj.store.users:
#             return True
#         elif request.user.is_superuser:
#             return True
#         return False