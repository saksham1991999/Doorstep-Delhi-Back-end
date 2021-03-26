from django.db import models
from django_countries.fields import CountryField


class Store(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField()
    users = models.ManyToManyField("accounts.User")
    address = models.ForeignKey("accounts.Address", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    shipping_zones = models.ManyToManyField("store.ShippingZone")


class ShippingZone(models.Model):
    name = models.CharField(max_length=100)
    countries = CountryField(multiple=True, default=[], blank=True)
    default = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


shipping_method_type_choices = (
    ("S", "Free Shipping"),
    ("FS", "Fast Shipping"),
    ("DS", "Default Shipping"),
)


class ShippingMethod(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=30, choices=shipping_method_type_choices)
    shipping_zone = models.ForeignKey(
        ShippingZone, related_name="shipping_methods", on_delete=models.CASCADE
    )
    excluded_products = models.ManyToManyField(
        "product.Product", blank=True
    )
    maximum_delivery_days = models.PositiveIntegerField(null=True, blank=True)
    minimum_delivery_days = models.PositiveIntegerField(null=True, blank=True)
