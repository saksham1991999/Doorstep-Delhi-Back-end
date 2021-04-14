from django.urls import path, include
from rest_framework.routers import DefaultRouter
from wishlist.views import WishlistItemAPIViewSet

router = DefaultRouter()
router.register("wishlist_items", WishlistItemAPIViewSet, basename="wishlist_items")


urlpatterns = [
    path("", include(router.urls)),
]
