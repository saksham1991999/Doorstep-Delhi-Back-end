from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from datetime import datetime

from .models import Store, ShippingZone, ShippingMethod
from accounts.models import Address
from accounts.serializers import AddressSerializer


class ShippingMethodSerializers(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = [
            'name',
            'type',
            'shipping_zone',
            'excluded_products',
            'maximum_delivery_days',
            'minimum_delivery_days',
        ]

class ShippingZoneSerializers(serializers.ModelSerializer):
    Shipping_Method = ShippingMethodSerializers(many=True)
    class Meta:
        model = ShippingZone
        fields = [
            'name',
            'countries',
            'default',
            'description',
            'Shipping_Method',
        ]



class StoreSerializers(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Store 
        fields = [
            'name',
            'email',
            'users',
            'address',
            'created_at',
            'shipping_zones'
        ]
    def get_address(self, obj):
        user = self.context['request'].user
        address = Address.objects.get(user=user)
        data = AddressSerializer(address).data
        return data