from django.contrib import admin
import nested_admin
from .models import User, Address

admin.site.site_header = "Doorstep Delhi"


class AddressInline(nested_admin.NestedStackedInline):
    model = Address


class UserAdmin(nested_admin.NestedModelAdmin):
    model = User
    inlines = [AddressInline]


admin.site.register(User, UserAdmin)
