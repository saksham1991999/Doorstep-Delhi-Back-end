from django.shortcuts import render
from .serializers import AddressSerializer
from .models import Address, User
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from accounts.permissions import IsWebsiteOwnerorAdmin
# Create your views here.

""" Viewset to Display all users """


""" Viewset to display current user """

""" Viewset to display current user address """


class PersonalAddressViewset(viewsets.ModelViewSet):
    permission_classes = [IsWebsiteOwnerorAdmin]
    serializer_class = AddressSerializer

    def get_queryset(self):
        addresses = Address.objects.all()
        return addresses

    @action(detail=False, methods=["get"])
    def my_address(self, request, *args, **kwargs):
        try:
            my_addresses = Address.objects.filter(user=request.user)
        # websites = Website.objects.exclude(user=request.user).exclude(id__in = surfed_websites)
            serializer = AddressSerializer(my_addresses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Error. You need to log in !", status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def create_address(self, request, pk, *args, **kwargs):
        try:
            Address = self.get_object()
            user = request.user
            serializer = AddressSerializer()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Error", status=status.HTTP_400_BAD_REQUEST)
