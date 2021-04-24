from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q
from datetime import date, datetime

from .serializers import (OrderSerializer, OrderLineSerializer, OrderEventSerializer,
                          InvoiceSerializers, GiftCardSerializers, VoucherSerializers,
                          SaleSerializers, CouponInputSerializers)
from .models import (Order, OrderLine, OrderEvent, Invoice, GiftCard, Voucher, Sale)
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin, IsOwnerReadOnlyOrAdmin


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerReadOnlyOrAdmin]

    def get_queryset(self):
        orders = Order.objects.all()
        if not self.request.user.is_superuser:
            orders = orders.filter(user = self.request.user)
        return orders

    @action(detail=True, methods=['get'])
    def invoice(self, request, pk=None):
        order = self.get_object()
        order.total_net_price = order.shipping_price + order.undiscounted_total_net_amount
        pass

    @action(detail=True, methods = ['post'])
    def coupon(self,request, pk=None):
        permission_classes = [IsAuthenticated]
        serializer = CouponInputSerializers(data = request.data)
        if serializer.is_valid():
            category = serializer.validated_data['category']
            if category=='giftcard':
                giftcard = get_object_or_404(GiftCard, code=serializer.validated_data['code'])
                if(giftcard.isactive):
                    giftcard.last_used_on = date.today()
                    order = self.get_object()
                    discount = 0
                    if giftcard.current_balance_amount > order.total_net_amount :
                        discount = order.total_net_amount
                        giftcard.current_balance_amount = giftcard.current_balance_amount - discount
                    else:
                        discount = giftcard.current_balance_amount
                        giftcard.current_balance_amount = 0
                        giftcard.is_active = False
                    order.total_net_amount = order.total_net_amount - discount
                    return order
                else:
                    return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
            else:
                voucher = get_object_or_404(Voucher, code=serializer.validated_data['code'])
                order = self.get_object()
                order.voucher = voucher
                voucher.used = voucher.user + 1
                if voucher.apply_once_per_customer == True:
                    pass
                if voucher.type == "shipping":
                    order.shipping_price = order.shipping_price - (order.shipping_price*(voucher.value/100))
                elif voucher.type == "entire_order":
                    order.total_net_amount = order.total_net_amount - (order.total_net_amount*(voucher.value/100))
                return order

    
    @action(detail=True, methods = ['post'])
    def payment(self, request, pk=None):
        pass    

    @action(detail=True, methods = ['post'])
    def return_request(self, request, pk=None):
        pass
    
    @action(detail=True, methods=['post'])
    def payment_status(self, request, pk=None):
        pass

    @action(detail=False, methods=['get'], permission_classes=[IsOwnerReadOnlyOrAdmin])
    def cart(self, request):
        cart = Order.objects.filter(user=self.request.user, status='draft')
        if cart.exists():
            cart = cart[0]
        else:
            cart = Order.objects.create(user=self.request.user, status="draft")
        serializer = OrderSerializer(cart, many=False)
        return serializer.data


class OrderEventViewSet(viewsets.ModelViewSet):
    serializer_class = OrderEventSerializer
    permission_classes = [IsOwnerReadOnlyOrAdmin]
    queryset = OrderEvent.objects.all()


class GiftCardViewset(viewsets.ModelViewSet):
    serializer_class = GiftCardSerializers
    permission_classes = [IsAdminOrReadOnly]
    queryset = GiftCard.objects.all()

class VoucherViewset(viewsets.ModelViewSet):
    serializer_class = VoucherSerializers
    permission_classes = [IsAdminOrReadOnly]
    queryset = Voucher.objects.all()

class SaleViewset(viewsets.ModelViewSet):
    serializer_class = SaleSerializers
    permission_class = [IsAdminOrReadOnly]
    queryset = Sale.objects.all()
