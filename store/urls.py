from django.urls import path, include
from rest_framework.routers import DefaultRouter

from store.views import StoreViewset, ShippingZoneViewset


app_name = 'store'


router = DefaultRouter()
router.register('store', StoreViewset, basename='store')
router.register('zones',ShippingZoneViewset, basename='shippingzone')

urlpatterns = [
    path('', include(router.urls)),
]