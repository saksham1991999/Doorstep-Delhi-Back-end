from django.contrib import admin
import nested_admin
from .models import User, Address

admin.site.site_header = 'Doorstep Delhi'
admin.site.register(User)
admin.site.register(Address)

#Is this what you meant by Nested Admin?
""" 
class UserInline(nested_admin.NestedStackedInline):
    model = User
    fk_name = "default_shipping_address"
    #sortable_field_name = "position"

class AddressInline(nested_admin.NestedModelAdmin):
    inlines = [UserInline]

admin.site.register(Address, AddressInline)
"""