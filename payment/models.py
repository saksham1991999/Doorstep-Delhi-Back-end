from decimal import Decimal
from operator import attrgetter

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import JSONField

from .choices import (
    payment_charge_choices,
    transaction_kind_choices,
    transaction_error_choices,
)


class Payment(models.Model):
    gateway = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    to_confirm = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    charge_status = models.CharField(
        max_length=20, choices=payment_charge_choices, default="not-charged"
    )
    total = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )
    captured_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )
    order = models.ForeignKey(
        "shop.Order", null=True, related_name="payments", on_delete=models.PROTECT
    )

    billing_email = models.EmailField(blank=True)
    billing_first_name = models.CharField(max_length=256, blank=True)
    billing_last_name = models.CharField(max_length=256, blank=True)
    billing_company_name = models.CharField(max_length=256, blank=True)
    billing_address_1 = models.CharField(max_length=256, blank=True)
    billing_address_2 = models.CharField(max_length=256, blank=True)
    billing_city = models.CharField(max_length=256, blank=True)
    billing_city_area = models.CharField(max_length=128, blank=True)
    billing_postal_code = models.CharField(max_length=256, blank=True)
    billing_country_code = models.CharField(max_length=2, blank=True)
    billing_country_area = models.CharField(max_length=256, blank=True)

    cc_first_digits = models.CharField(max_length=6, blank=True, default="")
    cc_last_digits = models.CharField(max_length=4, blank=True, default="")
    cc_brand = models.CharField(max_length=40, blank=True, default="")
    cc_exp_month = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)], null=True, blank=True
    )
    cc_exp_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1000)], null=True, blank=True
    )

    payment_method_type = models.CharField(max_length=256, blank=True)

    customer_ip_address = models.GenericIPAddressField(blank=True, null=True)
    extra_data = models.TextField(blank=True, default="")
    return_url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ("pk",)

    def __repr__(self):
        return "Payment(gateway=%s, is_active=%s, created=%s, charge_status=%s)" % (
            self.gateway,
            self.is_active,
            self.created,
            self.charge_status,
        )


class Transaction(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    payment = models.ForeignKey(
        Payment, related_name="transactions", on_delete=models.PROTECT
    )
    kind = models.CharField(max_length=25, choices=transaction_kind_choices)
    is_success = models.BooleanField(default=False)
    action_required = models.BooleanField(default=False)
    action_required_data = JSONField(
        blank=True, default=dict, encoder=DjangoJSONEncoder
    )
    amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )
    error = models.CharField(
        choices=transaction_error_choices,
        max_length=256,
        null=True,
    )
    customer_id = models.CharField(max_length=256, null=True)
    gateway_response = JSONField(encoder=DjangoJSONEncoder)
    already_processed = models.BooleanField(default=False)
    searchable_key = models.CharField(max_length=512, null=True, blank=True)
