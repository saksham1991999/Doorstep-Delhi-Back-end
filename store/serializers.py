from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from datetime import datetime

from .models import Store, ShippingZone, ShippingMethod
from accounts.models import Address
from accounts.serializers import AddressSerializer


class ShippingMethodSerializer(serializers.ModelSerializer):
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


class ShippingZoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShippingZone
        fields = [
            'name',
            'countries',
            'default',
            'description',
        ]


class StoreSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
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