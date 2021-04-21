from django.shortcuts import render, get_object_or_404
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
from wishlist.models import Wishlist, WishlistItem
from wishlist.serializers import WishlistSerializer
from accounts.models import Address
from shop.serializers import OrderLineSerializers
from shop.models import Order, OrderLine
# Create your views here.


class ProductAPIViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer2
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        products = Product.objects.all()
        # serializer = ProductSerializer(products, many=True)
        return products  # Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductListSerilaizer(products, many=True)
        return Response(serializer.data)


class CategoryViewset(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

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
    
    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated]) # PERMISSION CLASSES and GET
    def add_to_wishlist(self, request, pk):
        
        current_user = request.user
        current_product_varaint = get_object_or_404(ProductVariant, id=pk)
        user_wishlist = Wishlist.objects.get_or_create(user = current_user)[0]

        user_wishlist.add_variant(current_product_varaint)
        user_wishlist.save()

        serializer = WishlistSerializer(user_wishlist, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    
    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def remove_from_wishlist(self, request, pk):
        
        current_user = request.user
        current_product_variant = get_object_or_404(ProductVariant, id = pk)

        wishlist_item = Wishlist.objects.get_or_create(user = current_user)[0]
        wishlist_item.remove_variant(current_product_variant)
        wishlist_item.save()

        serializer = WishlistSerializer(wishlist_item, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def add_to_cart(self,request,pk):
        current_user = request.user
        user_address = get_object_or_404(Address, user=current_user)
        order = get_object_or_404(Order, user=current_user, billing_address=user_address.billing_address, shipping_address=user_address.shipping_address)
        current_product_variant = get_object_or_404(ProductVariant, id = pk)
        
        if(Order.objects.filter(user=current_user).exists()):
            current_order = Order.objects.get_or_create(user=current_user)
            if(OrderLine.objects.filer(order=current_order, variant=current_product_variant).exists()):
                orderline = OrderLine.objects.get_or_create(order=current_order, variant=current_product_variant)
                orderline_quantity = orderline.quantity
                orderline.update(quantity= orderline_quantity+1)
                orderline.save()

                serializer = OrderLineSerializer(orderline)
                return Response(serializer.data, status=status.HTTP_200_OK)

            else:
                orderline = OrderLine.objects.get_or_create(order=current_order, variant=current_product_variant, quantity=1)
                orderline.save()
            
                serializer = OrderLineSerializer(orderline)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            current_order = Order.objects.get_or_create(user=current_user)
            current_product_variant = get_object_or_404(ProductVariant, id = pk)

            orderline = OrderLine.objects.get_or_create(order=current_order, variant=current_product_variant, quantity=1)
            orderline.save()
            
            serializer = OrderLineSerializer(orderline)
            return Response(serializer.data, status=status.HTTP_200_OK)



class WholesaleProductVariantViewset(viewsets.ModelViewSet):
    serializer_class = WholesaleProductVariantSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        wholesaleProductVariants = WholesaleProductVariant.objects.all()
        return wholesaleProductVariants

