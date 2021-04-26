from django.shortcuts import render, get_object_or_404, get_list_or_404
from .serializers import AddressSerializer, UserSerializer
from .models import Address, User
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsOwnerOrAdmin


class AddressViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = AddressSerializer

    def get_queryset(self):
        addresses = Address.objects.all()
        if not self.request.user.is_superuser:
            addresses = addresses.filter(user=self.request.user)
        return addresses


class UserViewSet(viewsets.ModelViewSet):
    permissions_classes = [IsOwnerOrAdmin]
    serializer_class = UserSerializer

    def get_queryset(self):
        users = User.objects.all()
        if not self.request.user.is_superuser:
            users = self.request.user
        return users

    @action(detail=True, methods=["get"], permissions_classes=[IsAuthenticated,])
    def adrresses(self, request, *args, **kwargs):
        addresses = get_list_or_404(Address, user=self.request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], permissions_classes=[IsAuthenticated,])
    def default_shipping_address(self, request, *args, **kwargs):
        address = request.user.default_shipping_address
        if address:
            serializer = AddressSerializer(address, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"Error": "You don't have a Default Shipping Address"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=["get"], permissions_classes=[IsAuthenticated,])
    def default_billing_address(self, request, *args, **kwargs):
        address = request.user.default_billing_address
        if address:
            serializer = AddressSerializer(address, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"Error": "You don't have a Default Shipping Address"}, status=status.HTTP_404_NOT_FOUND)


