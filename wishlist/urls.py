from django.urls import path, include
from rest_framework.routers import DefaultRouter
from wishlist.views import WishlistItemAPIViewSet

router = DefaultRouter()
router.register("wishlists", WishlistItemAPIViewSet, basename="wishlist-detail")


urlpatterns = [
    path("", include(router.urls)),
]
