from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from datetime import datetime

from .models import Order, OrderLine, OrderEvent, Invoice, GiftCard, Voucher, Sale

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
