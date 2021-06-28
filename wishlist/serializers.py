from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from datetime import datetime

from wishlist.models import Wishlist, WishlistItem
from product.serializers.product import WholesaleProductVariantListSerializer


class WishlistItemSerializer(serializers.ModelSerializer):
    wholesale_variants = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = WishlistItem
        fields = (
            "id",
            "product",
            "variants",
            "wholesale_variants",
            "created_at",
        )

    def get_wholesale_variants(self, obj):
        wholesale_variants = obj.wholesale_variants.all()
        serializer = WholesaleProductVariantListSerializer(wholesale_variants, many=True)
        return serializer.data


class WishlistSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    created_at = serializers.DateTimeField(read_only=True)
    items = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Wishlist
        fields = (
            "id",
            "user",
            "created_at",
            "items",
        )

    def get_items(self, obj):
        items = WishlistItem.objects.filter(wishlist=obj)
        serializer = WishlistItemSerializer(items, many=True)
        return serializer.data
