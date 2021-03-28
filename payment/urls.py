from django.urls import path, include
from rest_framework.routers import DefaultRouter

from payment.views import TransactionViewset

router = DefaultRouter()
router.register("transactions", TransactionViewset, basename="transactions")

urlpatterns = [
    path("", include(router.urls)),
]
