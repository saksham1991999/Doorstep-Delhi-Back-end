from django.urls import path, include
from rest_framework.routers import DefaultRouter

from payment.views import TransactionViewSet, PaymentViewSet

router = DefaultRouter()
router.register("payments", PaymentViewSet, basename="payment-detail")
router.register("transactions", TransactionViewSet, basename="transaction-detail")

urlpatterns = [
    path("", include(router.urls)),
]
