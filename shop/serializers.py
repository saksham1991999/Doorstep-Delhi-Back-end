from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from datetime import datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import Order, OrderLine, OrderEvent, Invoice, GiftCard, Voucher, Sale
from accounts.models import Address
from accounts.serializers import AddressSerializer

class OrderSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault)
    created = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Order
        fields = [
            'id',
            'created',
            'status', 
            'user', 
            'tracking_client_id', 
            'billing_address', 
            'shipping_address', 
            'shipping_method', 
            'shipping_price', 
            'total_net_amount', 
            'undiscounted_amount',
            'voucher',
            'gift_cards',
            'display_gross_price',
            'customer_note',
        ]
        read_only_fields = ('id','tracking_client_id',)        

class OrderListSerializers(serializers.ModelSerializer):
    pass


class OrderLineSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderLine
        fields = [
            'id',
            'order',
            'variant',
            'quantity',
            'quantity_fulfilled',
        ]



class OrderEventSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault)
    date = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = OrderEvent
        fields = [
            'user',
            'date',
            'type',
            'order',
        ]


class InvoiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
            'order', 
            'number', 
            'created', 
            'external_url', 
            'invoice_file', 
        ]


class GiftCardSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault)
    created = serializers.DateTimeField(read_only=True)
    class Meta:
        model = GiftCard
        fields = [
            'code', 
            'user', 
            'created', 
            'start_date', 
            'end_date', 
            'last_used_on', 
            'is_active', 
            'initial_balance_amount', 
            'current_balance_amount', 
        ]

class GiftCardListSerializers(serializers.ModelSerializer):
    pass



class VoucherSerializers(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = [
            'type',
            'name',
            'code',
            'usage_limit',
            'used',
            'start_date',
            'end_date',
            'apply_once_per_order',
            'apply_once_per_customer',
            'discount_value_type',
            'min_checkout_items_quantity',
            'products',
            'collections',
            'categories',
        ]

class VoucherListSerializers(serializers.ModelSerializer):
    pass

class SaleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = [
            'name',
            'type',
            'products',
            'categories',
            'collections',
            'start_date',
            'end_date',            
        ]


class CouponInputSerializers(serializers.Serializer):
    current_date = serializers.HiddenField(default=timezone.now)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault)
    code = serializers.CharField(max_length = 20)
    category = serializers.SerializerMethodField(read_only = True)

    def get_category(self):
        if self.code[:3]=="GFC":
            return "giftcard"
        else:
            return "voucher"

    def validate(self,data):
        if data['category']=="giftcard":
            code = get_object_or_404(GiftCard,code=data['code'])
            if not code:
                raise serializers.ValidationError("Invalid GiftCard")
            elif data['user'] != code.user :
                raise serializers.ValidationError("Giftcard doesn't link with current account")
            elif not (data['current_date'] >= code.start_date) :
                raise serializers.ValidationError("Using Giftcard early")
            elif not (data['current_date'] <= code.end_date) :
                raise serializers.ValidationError("Giftcard expired")
            else:
                return data

        else:
            code = get_object_or_404(Voucher,code=data['code'])
            if not code:
                raise serializers.ValidationError("Invalid Voucher")
            elif not (data['current_date'] >= code.start_date) :
                raise serializers.ValidationError("Using Voucher early")
            elif not (data['current_date'] <= code.end_date) :
                raise serializers.ValidationError("Voucher expired")
            elif not (code.used <= code.usage_limit):
                raise serializers.ValidationError("Voucher using limit surpassed")
            else:
                return data


class AddressInputSerializer(serializers.Serializer):
    default_address = serializers.SerializerMethodField(read_only = True)
    address = serializers.CharField(max_length=None, min_length=None, allow_blank=True, trim_whitespace=True)

    def get_default_address(self, obj):
        user = self.context['request'].user
        address = Address.objects.get(user=user)
        data = AddressSerializer(address).data
        return data

class PaymentSerializer(serializers.Serializer):
    date = serializers.HiddenField(default=timezone.now)
    



    