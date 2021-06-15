from django.shortcuts import render
from .models import Room, RoomOrder, RoomUser, RoomWishlistProduct, UserOrderLine
from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework.decorators import action
from room.serializers import RoomOrderSerializer, RoomSerializer, RoomListSerializer, RoomUserSerializer, RoomWishlistProductSerializer, UserOrderLineSerializer

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


# class UserOrderLineViewset(viewsets.ModelViewSet):
#     serializer_class = UserOrderLineSerializer
#     permission_classes = []
#     queryset = UserOrderLine.objects.all()    
    
#     # def list(self, request):
#     #     queryset = self.queryset
#     #     serializer = UserOrderLineSerializer(queryset, many=True)
#     #     return Response(serializer.data)

