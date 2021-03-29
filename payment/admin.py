from django.contrib import admin
import nested_admin
from nested_admin import NestedStackedInline, NestedModelAdmin
from payment.models import Transaction, Payment

# Register your models here.

#admin.site.register(Payment)
admin.site.register(Transaction)




class TransactionAdmin(NestedStackedInline):
    model = Transaction


class PaymentInline(NestedModelAdmin):
    model = Payment
    inlines = [TransactionAdmin]
    class Meta:
        verbose_name = ("InlinePayment")

admin.site.register(Payment, PaymentInline)