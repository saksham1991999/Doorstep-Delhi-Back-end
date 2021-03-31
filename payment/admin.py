from django.contrib import admin
import nested_admin
from nested_admin import NestedInlineModelAdmin, NestedModelAdmin
from payment.models import Transaction, Payment


# Register your models here.


class TransactionAdmin(NestedInlineModelAdmin):
    model = Transaction


class PaymentInline(NestedModelAdmin):
    model = Payment
    inlines = [TransactionAdmin]


admin.site.register(Payment, PaymentInline)
