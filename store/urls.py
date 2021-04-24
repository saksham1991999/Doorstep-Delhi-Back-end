from django.urls import path, include
from rest_framework.routers import DefaultRouter

from store.views import StoreViewSet, ShippingZoneViewSet, ShippingMethodViewSet


app_name = 'store'


router = DefaultRouter()
router.register('stores', StoreViewSet, basename='store-detail')
router.register('zones', ShippingZoneViewSet, basename='zone-detail')
router.register('methods', ShippingMethodViewSet, basename='method-detail')

urlpatterns = [
    path('', include(router.urls)),
]