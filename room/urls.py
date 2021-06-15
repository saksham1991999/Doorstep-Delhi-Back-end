# chat/urls.py
from django.urls import path, include

from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("rooms-view", views.RoomViewset, basename="rooms-detail")
router.register("rooms-wishlist", views.RoomWishlistProductViewset, basename="rooms-wishlist")
# router.register("user-orders", views.UserOrderLineSerializer, basename="user-orders")


urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    path("rooms/", include(router.urls)),
]
