from django.contrib import admin
import nested_admin
from product.models import (
    Category,
    ProductType,
    Variation,
    Customization,
    Product,
    ProductVariant,
    WholesaleProductVariant,
    ProductImage,
    VariantImage,
    WholesaleVariantImage,
    CollectionProduct,
    Collection,
)


# Register your models here.

admin.site.register(Category)
#admin.site.register(ProductType)
admin.site.register(Variation)
admin.site.register(Customization)
##admin.site.register(Product)
admin.site.register(ProductVariant)
#admin.site.register(WholesaleProductVariant)
##admin.site.register(ProductImage)
admin.site.register(VariantImage)#
##admin.site.register(WholesaleVariantImage)
##admin.site.register(CollectionProduct)
#admin.site.register(Collection)



class WholesaleVariantImageAdmin(nested_admin.NestedInlineModelAdmin):
    model = WholesaleVariantImage


class WholesaleProductVariantAdmin(nested_admin.NestedModelAdmin):
    model = WholesaleProductVariant
    inlines = [WholesaleVariantImageAdmin]

admin.site.register(WholesaleProductVariant, WholesaleProductVariantAdmin)






class CollectionProductAdmin(nested_admin.NestedStackedInline):
    model = CollectionProduct

class CollectionAdmin(nested_admin.NestedModelAdmin):
    model = Collection
    inlines = [CollectionProductAdmin]
admin.site.register(Collection, CollectionAdmin)


class ProductImageAdmin(nested_admin.NestedStackedInline):
    model = ProductImage

class ProductAdmin(nested_admin.NestedStackedInline):
    model = Product
    inlines = [ProductImageAdmin]

class ProductTypeAdmin(nested_admin.NestedModelAdmin):
    model = ProductType
    inlines = [ProductAdmin]
admin.site.register(ProductType,ProductTypeAdmin)
