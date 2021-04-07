from django.contrib import admin
import nested_admin
<<<<<<< HEAD
from nested_admin import NestedInlineModelAdmin, NestedModelAdmin
from payment.models import Transaction, Payment


# Register your models here.

class TransactionAdmin(NestedInlineModelAdmin):
    model = Transaction


class PaymentInline(NestedModelAdmin):
    model = Payment
    inlines = [TransactionAdmin]


admin.site.register(Payment, PaymentInline)
=======

from payment.models import Transaction, Payment


class TransactionInline(nested_admin.NestedTabularInline):
    model = Transaction
    extra = 0


class PaymentAdmin(nested_admin.NestedModelAdmin):
    model = Payment
    inlines = [TransactionInline]
    ordering = ['modified']
    list_display = [
                    'billing_first_name',
                    'billing_email',
                    'order',
                    'captured_amount',
                    'charge_status'
                    ]
    list_editable = [
        'charge_status',
    ]
    list_display_links = [
                    'billing_first_name',
                    'billing_email',
                    'order',
                    'captured_amount'
                    ]
    search_fields = [
                    'billing_first_name',
                    'billing_last_name',
                    'billing_company_name',
                    'billing_address_1',
                    'billing_address_2',
                    'billing_city',
                    'billing_email',
                    'order',
                    'captured_amount',
                    'charge_status',
                    ]
    list_filter = [
                    'payment_method_type',
                    'gateway',
                    'billing_city',
                    'is_active',
                    'to_confirm',
                    'charge_status',
                    ]


admin.site.register(Payment, PaymentAdmin)
>>>>>>> 4f3ae586f40b52b5a2cb4f462a8f75ff579f07d8
