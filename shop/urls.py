from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shop.views import OrderEventViewSet, GiftCardViewset, OrderLineViewSet, VoucherViewset, SaleViewset, OrderViewSet


app_name = 'shop'


router = DefaultRouter()
router.register('event', OrderEventViewSet, basename='order-event')
router.register('giftcard', GiftCardViewset, basename='giftcard')
router.register('voucher', VoucherViewset, basename='voucher')
router.register('sales', SaleViewset, basename='sale')
router.register('order', OrderViewSet, basename='order')
router.register('orderline',OrderLineViewSet, basename = "order-line")

urlpatterns = [
    path('', include(router.urls)),
]