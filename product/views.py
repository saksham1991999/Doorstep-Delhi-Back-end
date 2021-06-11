import datetime

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
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

from product.models import (
    Category,
    SubCategory,
    ProductType,
    Variation,
    Customization,
    Product,
    ProductVariant,
    WholesaleProductVariant,
    ProductImage,
    VariantImage,
    WholesaleVariantImage,
    ProductReview,
    ProductReviewFile,
    CollectionProduct,
    Collection,
)
from product.permissions import IsWebsiteOwnerorAdmin, IsAdminOrReadOnly
from product.serializers import *  # """ NEED TO CHANGE ASAP """
from wishlist.models import Wishlist, WishlistItem
from wishlist.serializers import WishlistSerializer
from accounts.models import Address
from shop.serializers import OrderLineSerializer
from shop.models import Order, OrderLine


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.all()

    @method_decorator(cache_page(60 * 60 * 24))
    def list(self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 60 * 24))
    @action(detail=True, methods=['get'], name='Sub-Categories')
    def set_password(self, request, pk=None):
        category = self.get_object()
        sub_categories = SubCategory.objects.filter(category=category)
        serializer = SubCategorySerializer(sub_categories, many=True)
        return Response(serializer.data)


class ProductTypeViewSet(viewsets.ModelViewSet):
    serializer_class = ProductTypeSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = ProductType.objects.all()

    @method_decorator(cache_page(60 * 60 * 24))
    def list(self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class VariationViewSet(viewsets.ModelViewSet):
    serializer_class = VariationSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Variation.objects.all()

    @method_decorator(cache_page(60 * 60 * 24))
    def list(self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class CustomizationViewSet(viewsets.ModelViewSet):
    serializer_class = CustomizationSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Customization.objects.all()

    @method_decorator(cache_page(60 * 60 * 24))
    def list(self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Collection.objects.all()

    @method_decorator(cache_page(60 * 60 * 24))
    def list(self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 60 * 24))
    @action(detail=True, methods=['get'])
    def products(self, request, pk = None):
        collection = self.get_object()
        products = collection.products.all()
        serializer = ProductListSerilaizer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        if cache.get(products):
            products = cache.get(products)
        else:
            products = Product.objects.filter(visible_in_listings=True)
            # ca
        return products
    
    def list(self, request, *args, **kwargs):
        products = self.get_queryset()
        serializer = ProductListSerilaizer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductImageViewSet(viewsets.ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        images = ProductImage.objects.all()
        return images


class ProductVariantViewSet(viewsets.ModelViewSet):
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        productVariants = ProductVariant.objects.all()
        return productVariants
    
    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def add_to_wishlist(self, request, pk):
        product_variant = self.get_object()
        wishlist, created = Wishlist.objects.get_or_create(user = request.user)
        wishlist_item = wishlist.add_variant(product_variant)
        serializer = WishlistSerializer(wishlist, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def remove_from_wishlist(self, request, pk):
        product_variant = self.get_object()
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist.remove_variant(product_variant)
        serializer = WishlistSerializer(wishlist, many=False)
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


class WholesaleProductVariantViewSet(viewsets.ModelViewSet):
    serializer_class = WholesaleProductVariantSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        wholesale_product_variants = WholesaleProductVariant.objects.all()
        return wholesale_product_variants

