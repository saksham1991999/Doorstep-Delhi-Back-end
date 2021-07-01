from django.shortcuts import render
from .models import Room, RoomOrder, RoomUser, RoomWishlistProduct, UserOrderLine
from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework.decorators import action
from room.serializers import RoomOrderSerializer, RoomSerializer, RoomListSerializer, RoomUserSerializer, RoomWishlistProductSerializer, RoomOrderLineSerializer
from shop.models import OrderEvent
from django.db.models import Q

def index(request):
    return render(request, 'room/index.html', {})

def room(request, room_name):
    room = Room.objects.filter(name=room_name)[0]

    return render(request, 'room/room.html', {
        'room_name': room_name,
        'room' : room
    })

class RoomViewset(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = []
    queryset = Room.objects.all()

    def list(self, request):
        queryset = self.queryset
        serializer = RoomListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], name='room-users')
    def users(self, request, pk=None):
        users = RoomUser.objects.filter(room__id=pk)
        serializer = RoomUserSerializer(users, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], name='room-orders')
    def room_order(self, request, pk=None):
        orders = RoomOrder.objects.filter(room__id=pk)
        serializer = RoomOrderSerializer(orders, many=True)
        return Response(serializer.data)

class RoomWishlistProductViewset(viewsets.ModelViewSet):
    serializer_class = RoomWishlistProductSerializer
    permission_classes = []
    queryset = RoomWishlistProduct.objects.all()

    def list(self, request):
        queryset = self.queryset
        serializer = RoomWishlistProductSerializer(queryset, many=True)
        return Response(serializer.data)


class UserOrderLineViewSet(viewsets.ModelViewSet):         #verify
    serializer_class = RoomOrderLineSerializer
    permission_classes = []

    def get_queryset(self):
            
        userorderlines = UserOrderLine.objects.all()
        orderevents =OrderEvent.objects.all()
        if not self.request.user.is_superuser:
            Roomorderlines = userorderlines.filter(user = self.request.user)
            Roomorderevents = orderevents.filter(user = self.request.user)

        if self.request.query_params.get("status", None):

            status = self.request.query_params.get("status", None)

            if status == "unpaid":
                userorderlines = userorderlines.filter(
                    Q(order_status_iexact = "draft")
                )
            elif status == "shipped":
                userorderlines = userorderlines.filter(
                    order_status_in = ['partially_fulfilled','unfulfilled']
                )

            elif status == "in_dispute":
                orderevents = orderevents.filter(
                    type__in = map(lambda x:x.upper(), ['fulfillment_canceled','payment_failed','payment_voided','other'])
                    )
                orderlines = UserOrderLine.objects.filter(
                    Q(order_in = orderevents.values_list('order', flat=True)) | Q(orderstatus_iexact = "unconfirmed")
                )
            
            elif status == "to_be_shipped":
                orderevents = orderevents.filter(
                Q(type__iexact = "confirmed")
            )
                orderlines = UserOrderLine.objects.filter(order__in = orderevents.values_list('order', flat=True))

            
        return userorderlines