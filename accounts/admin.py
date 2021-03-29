from django.contrib import admin
import nested_admin
from .models import User, Address

admin.site.site_header = "Doorstep Delhi"


class AddressInline(nested_admin.NestedStackedInline):
    model = Address


class UserAdmin(admin.ModelAdmin):
    model = User
    inlines = [AddressInline]


admin.site.register(User, UserAdmin)
"""
admin.site.register(User)


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "full_name",
        "street_address_1",
        "street_address_2",
        "city",
        "state",
        "postal_code",
        "country",
        "country_area",
        "phone",
    ]
    ordering = ["city", "state", "postal_code", "country", "country_area"]
    search_fields = [
        "user__profile_pic",
        # "user__default_shipping_address",
        # "user__default_billing_address",
        "full_name",
        "street_address_1",
        "street_address_2",
        "city",
        "state",
        "postal_code",
        "country",
        "country_area",
        "phone",
    ]


admin.site.register(Address, AddressAdmin)

# Is this what you meant by Nested Admin?
""" 


