from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product.views import ProductAPIViewSet

router = DefaultRouter()
router.register("products/", ProductAPIViewSet, basename="products")

urlpatterns = [
    path("", include(router.urls)),
]
