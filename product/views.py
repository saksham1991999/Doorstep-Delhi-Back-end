from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAdminUser,
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from django.db.models import Q
import datetime

from product.serializers import *  # """ NEED TO CHANGE ASAP """

# Create your views here.


class ProductAPIViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = []

    def get_queryset(self):
        products = Product.objects.all()
        # serializer = ProductSerializer(products, many=True)
        return products  # Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def list_display(self, request):
        try:
            products = Product.objects.all()
            serializer = ProductsListDisplay(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("ERROR !!!", status=status.HTTP_400_BAD_REQUEST)
