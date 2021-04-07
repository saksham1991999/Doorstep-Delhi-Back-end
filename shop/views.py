from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q
import datetime

from .serializers import ( OrderSerializers, OrderLineSerializers, OrderEventSerializers,
                         InvoiceSerializers, GiftCardSerializers, VoucherSerializers,
                         SaleSerializers)

from .models import (Order, OrderLine, OrderEvent, Invoice, GiftCard, Voucher, Sale)
from .permissions import IsAdminOrReadOnly


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializers
    permission_classes = [IsAdminOrReadOnly]
    def get_queryset(self):
        return Order.objects.get(user=self.request.user)

    @action(detail=True, methods=['post'])
    def invoice(self, request, pk=None):
        order = self.get_object()
        pass

    @action(detail=True, methods = ['post'])
    def coupon(self, request, pk=None):
        pass

    @action(detail=True, methods = ['post'])
    def giftcard(self, request, pk=None):
        pass

    @action(detail=True, methods = ['post'])
    def voucher(self, request, pk=None):
        pass

    @action(detail=True, methods = ['post'])
    def payment(self, request, pk=None):
        pass    

    @action(detail=True, methods = ['post'])
    def return_request(self, request, pk=None):
        pass





class OrderEventViewset(viewsets.ModelViewSet):
    serializer_class = OrderEventSerializers
    permission_classes = [IsAdminOrReadOnly]
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
