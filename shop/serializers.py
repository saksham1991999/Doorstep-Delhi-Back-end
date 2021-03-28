from rest_framework import serializers
from shop.models import Order
from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = [
            "created",
            "status",
            "user",
            "tracking_client_id",
            "billing_address",  # NEED SERIALIZER
            "shipping_address",  # NEED SERIALIZER
            "shipping_method",  # NEED SERIALIZER
            "shipping_price",
            "total_net_amount",
            "undiscounted_total_net_amount",
            "voucher",  # NEED TO ADD A SERIALIZER
            "gift_cards",  # NEED A SERIALIZER
            "display_gross_prices",
            "customer_note",
        ]
