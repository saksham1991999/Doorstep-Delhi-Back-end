from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shop.views import OrderEventViewset, GiftCardViewset, VoucherViewset, SaleViewset, OrderViewSet


app_name = 'shop'


router = DefaultRouter()
router.register('event', OrderEventViewset, basename='order-event')
router.register('giftcard', GiftCardViewset, basename='giftcard')
router.register('voucher', VoucherViewset, basename='voucher')
router.register('sales', SaleViewset, basename='sale')
# router.register('order', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]