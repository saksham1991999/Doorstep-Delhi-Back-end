from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from payment.models import Transaction, Payment
from shop.serializers import OrderSerializer

class PaymentSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(read_only=True)
    modified = serializers.DateTimeField(read_only=True) 
    order = OrderSerializer()
    class Meta:
        model = Payment
        fields = [
            'gateway',
            'is_active',
            'to_confirm',
            'created',
            'modified',
            'charge_status',
            'total',
            'captured_amount',
            'order',
            'billing_email',
            'billing_first_name',
            'billing_last_name',
            'billing_company_name',
            'billing_address_1',
            'billing_address_2',
            'billing_city',
            'billing_city_area',
            'billing_postal_code',
            'billing_country_code',
            'billing_country_area',

            'cc_first_digits',
            'cc_last_digits',
            'cc_brand',
            'cc_exp_month',
            'cc_exp_year',
            'payment_method_type',
            'customer_ip_address',
            'extra_data',
            'return_url'
        ]

class TransactionSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(read_only=True)
    payment = PaymentSerializer(many=False)

    class Meta:
        model = Transaction
        fields = [
            'created',
            'payment',
            'kind',
            'is_success',
            'action_required',
            'amount',
            'error',
            'customer_id',
            'gateway_response',
            'already_processed',
            'searchable_key'
        ]