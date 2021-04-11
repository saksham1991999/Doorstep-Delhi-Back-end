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
from product.permissions import IsWebsiteOwnerorAdmin, IsAdminOrReadOnly

from product.serializers import *  # """ NEED TO CHANGE ASAP """
from wishlist.models import Wishlist

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
    permission_classes = [IsAdminOrReadOnly()]

    def get_queryset(self):
        categories = Category.objects.all()
        return categories


class ProductTypeViewset(viewsets.ModelViewSet):
    serializer_class = ProductTypeSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        productTypes = ProductType.objects.all()
        return productTypes

class VariationViewset(viewsets.ModelViewSet):
    serializer_class = VariationSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        variations = Variation.objects.all()
        return variations

class CustomizationViewset(viewsets.ModelViewSet):
    serializer_class = CustomizationSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        customizations = Customization.objects.all()
        return customizations

class ProductViewset(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        products = Product.objects.all()
        return products

class ProductImageViewset(viewsets.ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        productImages = ProductImage.objects.all()
        return productImages

class VariantImageViewset(viewsets.ModelViewSet):
    serializer_class = VariantImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        variantImages = VariantImage.objects.all()
        return variantImages

class WholesaleVariantImageViewset(viewsets.ModelViewSet):
    serializer_class = WholesaleVariantImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        wholesaleVariantImages = WholesaleVariantImage.objects.all()
        return wholesaleVariantImages

class CollectionProductViewset(viewsets.ModelViewSet):
    serializer_class = CollectionProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        collectionProducts = CollectionProduct.objects.all()
        return collectionProducts

class CollectionViewset(viewsets.ModelViewSet):
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        collections = Collection.objects.all()
        return collections

class ProductVariantViewset(viewsets.ModelViewSet):
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        productVariants = ProductVariant.objects.all()
        return productVariants
    
    @action(detail=True, methods=["get","post"])
    def add_to_wishlist(self, request, pk):
        try:
            current_user = request.user
            current_product_variant = ProductVariant.objects.get(id = pk)

            new_wishlist_item = Wishlist.objects.create(user = current_user)
            new_wishlist_item.add_variant(self, current_product_variant)
            new_wishlist_item.save()

            serializer = ProductVariantSerializer(new_wishlist_item, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except:
            return Response("ERROR !!!", status=status.HTTP_400_BAD_REQUEST)


class WholesaleProductVariantViewset(viewsets.ModelViewSet):
    serializer_class = WholesaleProductVariantSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        wholesaleProductVariants = WholesaleProductVariant.objects.all()
        return wholesaleProductVariants

