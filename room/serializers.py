from django.db import models
from shop.serializers import OrderSerializer
from typing import AsyncContextManager
from rest_framework import serializers
from room.models import Message, Room, RoomUser,RoomWishlistProduct,WishlistProductVote,RoomOrder, RoomOrderLine, UserOrderLine, OrderEvent,Invoice, Message
from product.serializers2 import WholesaleProductVariantSerializer
from accounts.serializers import AddressSerializer, UserSerializer
from store.serializers import PickupPointSerializer, ShippingMethodSerializer

class RoomSerializer(serializers.ModelSerializer):
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = Room
        fields = [
            "id",
            "name",
            "title",
            "description",
            "image",
            "created_at",
            "deleted_at",
            "users",
        ]

class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            "id",
            "name",
            "title",
            "image",
        ]

class RoomUserSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(
    #     default=serializers.CurrentUserDefault()
    # )
    user = UserSerializer()
    joined_at = serializers.ReadOnlyField()

    class Meta:
        model = RoomUser
        fields = [
            "id",
            "user",
            "role",
            "joined_at",
            "left_at"
        ]

class RoomWishlistProductSerializer(serializers.ModelSerializer):
    room = RoomSerializer()
    wholesale_variant = WholesaleProductVariantSerializer()
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    added_on = serializers.ReadOnlyField()

    class Meta:
        model = RoomWishlistProduct
        fields = [
            "id",
            "room",
            "wholesale_variant",
            "user",
            "added_on",
            "votes",
        ]

class WishlistProductVoteSerializer(serializers.ModelSerializer):
    product = RoomWishlistProductSerializer()
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = WishlistProductVote
        fields = [
            "id",
            "product",
            "user"
        ]

class RoomOrderSerializer(serializers.ModelSerializer):
    room = RoomSerializer()
    billing_address = AddressSerializer()
    shipping_address = AddressSerializer()
    pickup_point = PickupPointSerializer()
    shipping_method = ShippingMethodSerializer()

    class Meta:
        model = RoomOrder
        fields = [
            "id",
            "room",
            "status",
            "tracking_client_id",
            "billing_address",
            "shipping_address",
            "pickup_point",
            "shipping_method",
            "shipping_price",
            "total_net_amount",
            "undiscounted_total_net_amount"
        ]


class RoomOrderLineSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    variant = WholesaleProductVariantSerializer()
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = RoomOrderLine
        fields = [
            "id",
            "order",
            "variant",
            "created_at"
        ]

class UserOrderLineSerializer(serializers.ModelSerializer):
    product = RoomOrderLineSerializer()
    updated_at = serializers.ReadOnlyField()

    class Meta:
        model = UserOrderLine
        fields = [
            "id",
            "product",
            "quantity",
            "quantity_fulfilled",
            "updated_at",
        ]

class OrderEventSerializer(serializers.ModelSerializer):
    order = RoomOrderSerializer()
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = OrderEvent
        fields = [
            "id",
            "date",
            "type",
            "order",
            "user",
        ]

class InvoiceSerializer(serializers.ModelSerializer):
    order = RoomOrderSerializer()
    invoice_file = serializers.FileField()
    externl_url = serializers.URLField()

    class Meta:
        model = Invoice
        fields = [
            "id",
            "order",
            "number",
            "created",
            "external_url",
            "invoice_file"
        ] 

class MessageSerializer(serializers.ModelSerializer):
    file_field = serializers.FileField(allow_empty_file = True)
    created_on = serializers.ReadOnlyField()
    room = RoomSerializer()
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Message
        fields = [
            "id",
            "file_field",
            "message_text",
            "user",
            "created_on",
            "room"
        ]
