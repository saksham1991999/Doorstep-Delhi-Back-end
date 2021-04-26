from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts.views import AddressViewSet, UserViewSet

router = DefaultRouter()
router.register("addresses", AddressViewSet, basename="address-detail")
router.register("users", UserViewSet, basename="user-detail")

urlpatterns = [
    path("", include(router.urls)),
]
