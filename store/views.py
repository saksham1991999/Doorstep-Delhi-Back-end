from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action

from .serializers import StoreSerializer, ShippingZoneSerializer, ShippingMethodSerializer, PickupPointSerializer
from .models import Store, ShippingZone, ShippingMethod, PickupPoint
from .permissions import IsAdminOrReadOnly, IsPickupPointOwner, IsStoreOwner
from shop.models import Order


class StoreViewSet(viewsets.ModelViewSet):
    serializer_class = StoreSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Store.objects.all()

    @action(detail=True, methods=["get"], permission_classes=[IsStoreOwner, ])
    def order_history(self, request, pk, *args, **kwargs):
        store = self.get_object()
        orders = RoomOrderLine.objects.filter(status__in = ("canceled", "fulfilled"), variant__store = store)
        data = RoomOrderLineSerializer(orders, many=True)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], permission_classes=[IsStoreOwner, ])
    def returns(self, request, pk, *args, **kwargs):
        store = self.get_object()
        orders = RoomOrderLine.objects.filter(status__in = ("returned", "partially returned"), variant__store=store)
        data = RoomOrderLineSerializer(orders, many=True)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], permission_classes=[IsStoreOwner, ])
    def new_orders(self, request, pk, *args, **kwargs):
        store = self.get_object()
        orders = RoomOrderLine.objects.filter(status__in=("unfulfilled", "partially fulfilled"), variant__store=store)
        data = RoomOrderLineSerializer(orders, many=True)
        return Response(data, status=status.HTTP_200_OK)


class ShippingZoneViewSet(viewsets.ModelViewSet):
    serializer_class = ShippingZoneSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = ShippingZone.objects.all()


class ShippingMethodViewSet(viewsets.ModelViewSet):
    serializer_class = ShippingMethodSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = ShippingMethod.objects.all()


class PikupPointViewSet(viewsets.ModelViewSet):
    serializer_class = PickupPointSerializer
    permission_classes = [IsPickupPointOwner]
    queryset = PickupPoint.objects.all()

    @action(detail=True, methods=["get"], permission_classes=[IsPickupPointOwner, ])
    def order_history(self, request, pk, *args, **kwargs):
        pickup_point = self.get_object()
        orders = pickup_point.orders.filter()
        user = request.user
        type = request.data["type"]
        # website_hit = WebsiteHit.objects.create(
        #     website=website, user=user, type=type
        # )
        # return Response("Done", status=status.HTTP_200_OK)
        # except:
        #     return Response("Error", status=status.HTTP_400_BAD_REQUEST)

