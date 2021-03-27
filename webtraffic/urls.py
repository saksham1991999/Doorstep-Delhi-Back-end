from django.urls import path, include
from rest_framework.routers import DefaultRouter

from webtraffic.views import WebsiteAPIViewSet


app_name = "webtraffic"


router = DefaultRouter()
router.register("websites", WebsiteAPIViewSet, basename="website")

urlpatterns = [
    path("", include(router.urls)),
]
