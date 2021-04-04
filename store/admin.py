from django.contrib import admin
import nested_admin

from .models import Store, ShippingZone, ShippingMethod
from product.admin import WholesaleProductVariantInline


class StoreAdmin(nested_admin.NestedModelAdmin):
    model = Store
    inlines = [WholesaleProductVariantInline]


class ShippingMethodInlineAdmin(nested_admin.NestedTabularInline):
    model = ShippingMethod
    extra = 0
    min_num = 1    


class ShippingZoneAdmin(nested_admin.NestedModelAdmin):
    inline = [ShippingMethodInlineAdmin]


admin.site.register(Store, StoreAdmin)
admin.site.register(ShippingZone, ShippingZoneAdmin)