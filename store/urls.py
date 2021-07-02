from django.db.models import base
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from store.views import StoreProductListViewSet, StoreViewSet, ShippingZoneViewSet, ShippingMethodViewSet, FullRegister


app_name = 'store'


router = DefaultRouter()
router.register('stores', StoreViewSet, basename='store-detail')
router.register('zones', ShippingZoneViewSet, basename='zone-detail')
router.register('methods', ShippingMethodViewSet, basename='method-detail')
# router.register("store_products",StoreProductListViewSet, basename= 'store-product-detail')


urlpatterns = [
    path('', include(router.urls)),
    path('full_register/', FullRegister.as_view())
]