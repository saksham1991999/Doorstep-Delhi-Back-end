from django.contrib import admin
import nested_admin

from .models import User, Address
from product.admin import ProductReviewInline

admin.site.site_header = 'Doorstep Delhi'


class AddressInline(nested_admin.NestedTabularInline):
    model = Address
    extra = 0


class UserAdmin(nested_admin.NestedModelAdmin):
    model = User
    inlines = [
        AddressInline,
        ProductReviewInline,
    ]
    ordering = ['first_name']
    list_display = [
                    'id',
                    'username',
                    'first_name',
                    'email',
                    'city'
                    ]
    list_display_links = [
                    'username',
                    'first_name',
                    'email',
                    'city'
                    ]
    search_fields = [
                    'username',
                    'first_name',
                    'email',
                    'default_billing_address__street_address_1',
                    'default_billing_address__street_address_2',
                    'city'
                    ]
    list_filter = [
                    'default_billing_address__state',
                    ]


admin.site.register(User, UserAdmin)


