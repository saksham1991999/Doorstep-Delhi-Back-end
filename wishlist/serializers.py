from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from datetime import datetime

from wishlist.models import Wishlist, WishlistItem
from product.serializers import *


class WishlistItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = WishlistItem
        fields = (
            "product",
            "variants",
            "created_at",
        )


class WishlistSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
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