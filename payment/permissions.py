from rest_framework.permissions import BasePermission


class IsPaymentOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.order.user == request.user


class IsTransactionOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.payment.order.user == request.user

