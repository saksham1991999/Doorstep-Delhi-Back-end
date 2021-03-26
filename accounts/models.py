from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django_countries.fields import Country, CountryField
from django.forms.models import model_to_dict

from phonenumber_field.modelfields import PhoneNumber, PhoneNumberField
from versatileimagefield.fields import VersatileImageField


class User(AbstractUser):
    profile_pic = VersatileImageField(upload_to="user-profile-pics",blank=True, null=True)
    default_shipping_address = models.ForeignKey(
        "accounts.Address", related_name="+", null=True, blank=True, on_delete=models.SET_NULL
    )
    default_billing_address = models.ForeignKey(
        "accounts.Address", related_name="+", null=True, blank=True, on_delete=models.SET_NULL
    )


class Address(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    full_name = models.CharField(max_length=512, blank=True)
    street_address_1 = models.CharField(max_length=256, blank=True)
    street_address_2 = models.CharField(max_length=256, blank=True)
    city = models.CharField(max_length=256, blank=True)
    state = models.CharField(max_length=128, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = CountryField()
    country_area = models.CharField(max_length=128, blank=True)
    phone = models.CharField(max_length = 15, blank=True)

    class Meta:
        ordering = ("pk",)

    def __str__(self):
        return self.full_name

    def as_data(self):
        """Return the address as a dict suitable for passing as kwargs.
        Result does not contain the primary key or an associated user.
        """
        data = model_to_dict(self, exclude=["id", "user"])
        if isinstance(data["country"], Country):
            data["country"] = data["country"].code
        if isinstance(data["phone"], PhoneNumber):
            data["phone"] = data["phone"].as_e164
        return data

    def get_copy(self):
        """Return a new instance of the same address."""
        return Address.objects.create(**self.as_data())