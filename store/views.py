from django.shortcuts import render
from rest_framework import viewsets

from .serializers import StoreSerializer, ShippingZoneSerializer, ShippingMethodSerializer
from .models import Store, ShippingZone, ShippingMethod
from .permissions import IsAdminOrReadOnly


class StoreViewSet(viewsets.ModelViewSet):
    serializer_class = StoreSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Store.objects.all()


class ShippingZoneViewSet(viewsets.ModelViewSet):
    serializer_class = ShippingZoneSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = ShippingZone.objects.all()


class ShippingMethodViewSet(viewsets.ModelViewSet):
    serializer_class = ShippingMethodSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = ShippingMethod.objects.all()


