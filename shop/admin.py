from django.contrib import admin
import nested_admin

from .models import Order, OrderLine, OrderEvent, Invoice, GiftCard, Voucher, Sale


class OrderLineAdmin(nested_admin.NestedStackedInline):
    model = OrderLine


class InvoiceAdmin(nested_admin.NestedStackedInline):
    model = Invoice


class OrderEventAdmin(nested_admin.NestedStackedInline):
    model = OrderEvent


class OrderAdmin(nested_admin.NestedModelAdmin):
    inline = [OrderLineAdmin, InvoiceAdmin, OrderEventAdmin,]
    list_display = ['id',
                    'user',
                    'tracking_client_id',
                    'total_net_amount',
                    'status',

                    ]
    list_editable = [
                    'status',
                    ]
    list_display_links = [
                    'user',
                    'tracking_client_id',
                    'total_net_amount'
                    ]
    list_filter = [
                    'status',
                    ]
    search_fields = [
                    'user',
                    'tracking_client_id',
                    'total_net_amount'
                    'status',
                    'customer_notes',
                    ]


class VoucherAdmin(nested_admin.NestedModelAdmin):
    list_display = [
                    'type',
                    'name',
                    'code',
                    'usage_limit',
                    'used',
                    ]
    list_editable = [
                    'usage_limit',
                    ]
    list_display_links = [
                    'type',
                    'name',
                    'code'
                    ]
    list_filter = [
                    'type',
                    'apply_once_per_order',
                    'apply_once_per_customer',
                    ]
    search_fields = [
                    'type',
                    'name',
                    'code',
                    ]


admin.site.register(Voucher, VoucherAdmin)
admin.site.register(GiftCard)
admin.site.register(OrderEvent)
admin.site.register(Order, OrderAdmin)
admin.site.register(Sale)
admin.site.register(OrderLine)
