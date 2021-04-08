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
from accounts.permissions import IsWebsiteOwnerorAdmin

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

class CategoryViewset(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsWebsiteOwnerorAdmin]

    def get_queryset(self):
        categories = Category.objects.all()
        return categories


class ProductTypeViewset(viewsets.ModelViewSet):
    serializer_class = ProductTypeSerializer
    permission_classes = [IsWebsiteOwnerorAdmin]

    def get_queryset(self):
        productTypes = ProductType.objects.all()
        return productTypes

class VariationViewset(viewsets.ModelViewSet):
    serializer_class = VariationSerializer
    permission_classes = [IsWebsiteOwnerorAdmin]

    def get_queryset(self):
        variations = Variation.objects.all()
        return variations

class CustomizationViewset(viewsets.ModelViewSet):
    serializer_class = CustomizationSerializer
    permission_classes = [IsWebsiteOwnerorAdmin]

    def get_queryset(self):
        customizations = Customization.objects.all()
        return customizations

class ProductViewset(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsWebsiteOwnerorAdmin]

    def get_queryset(self):
        products = Product.objects.all()
        return products
