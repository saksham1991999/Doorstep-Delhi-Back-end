from django.contrib import admin
from nested_admin import NestedInlineModelAdmin, NestedModelAdmin, NestedStackedInline
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
from store.models import Store


# Register your models here.
#admin.site.register(Customization)
#admin.site.register(ProductType)
class ProductVariantAdmin(NestedStackedInline):
    model = ProductVariant

class ProductAdmin(NestedStackedInline):
    model = Product
    inlines = [ProductVariantAdmin]

class ProductTypeAdmin(NestedModelAdmin):
    inlines = [ProductAdmin]

admin.site.register(ProductType, ProductTypeAdmin)

class CategoryAdmin(NestedModelAdmin):
    inlines = [ProductAdmin]

admin.site.register(Category, CategoryAdmin)

class VariationAdmin(NestedModelAdmin):
    inlines = [ProductVariantAdmin]
admin.site.register(Variation, VariationAdmin)

class WholesaleProductVariantAdmin(NestedStackedInline):
    model = WholesaleProductVariant

class VariationAdmin2(NestedStackedInline):
    model = Variation

class StoreAdmin(NestedStackedInline):
    model = Store

class ProductAdmin2(NestedModelAdmin):
    #model = Product
    inlines = [WholesaleProductVariantAdmin]#, VariationAdmin2, StoreAdmin]
admin.site.register(Product, ProductAdmin2)




"""
import nested_admin


class ProductTypeAdmin(nested_admin.NestedStackedInline):
    model = ProductType

class CategoryAdmin(nested_admin.NestedStackedInline):
    model = Category

class VariationAdmin(nested_admin.NestedStackedInline):
    model = Variation

class ProductVariantAdmin(nested_admin.NestedStackedInline):
    model = ProductVariant
    inlines = [VariationAdmin]

class ProductAdmin(nested_admin.NestedStackedInline):
    model = Product
    inlines = [ProductTypeAdmin, CategoryAdmin, ProductVariantAdmin]

class StoreAdmin(nested_admin.NestedInlineModelAdmin):
    model = Store

class WholesaleProductVariant(nested_admin.NestedStackedInline):
    model = WholesaleProductVariant
    inlines = [StoreAdmin, ProductAdmin, VariationAdmin]

class ProductImageAdmin(nested_admin.NestedStackedInline):
    model = ProductImage
    inlines = [ProductAdmin]



class VariantImageAdmin(nested_admin.NestedModelAdmin):
    #model = VariantImage
    inlines = [ProductVariantAdmin, ProductImageAdmin]

admin.site.register(VariantImage, VariantImageAdmin)

class WholesaleVariantImageAdmin(nested_admin.NestedModelAdmin):
    #model = WholesaleVariantImage
    inlines = [WholesaleProductVariant, ProductImage]

admin.site.register(WholesaleVariantImage, WholesaleVariantImageAdmin)

class CollectionAdmin(nested_admin.NestedStackedInline):
    model = Collection
    inlines = [ProductAdmin]

class CollectionProductAdmin(nested_admin.NestedModelAdmin):
    #model = CollectionProduct
    inlines = [CollectionAdmin, ProductAdmin]

admin.site.register(CollectionProduct, CollectionProductAdmin)
"""