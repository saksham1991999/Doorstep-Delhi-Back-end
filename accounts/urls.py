from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts.views import PersonalAddressViewset

router = DefaultRouter()
router.register("personal_address", PersonalAddressViewset, basename="personal_address")

urlpatterns = [
    path("", include(router.urls)),
]
