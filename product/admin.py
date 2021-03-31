from django.contrib import admin
from nested_admin import NestedInlineModelAdmin, NestedModelAdmin
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

class ProductAdmin(NestedInlineModelAdmin):
    model = Product

class ProductTypeAdmin(NestedModelAdmin):
    inlines = [ProductAdmin]

admin.site.register(ProductType, ProductTypeAdmin)

"""
class ProductTypeAdmin(nested_admin.NestedInlineModelAdmin):
    model = ProductType

class CategoryAdmin(nested_admin.NestedInlineModelAdmin):
    model = Category

class VariationAdmin(nested_admin.NestedInlineModelAdmin):
    model = Variation

class ProductVariantAdmin(nested_admin.NestedInlineModelAdmin):
    model = ProductVariant
    inlines = [VariationAdmin]

class ProductAdmin(nested_admin.NestedInlineModelAdmin):
    model = Product
    inlines = [ProductTypeAdmin, CategoryAdmin, ProductVariantAdmin]

class StoreAdmin(nested_admin.NestedInlineModelAdmin):
    model = Store

class WholesaleProductVariant(nested_admin.NestedInlineModelAdmin):
    model = WholesaleProductVariant
    inlines = [StoreAdmin, ProductAdmin, VariationAdmin]

class ProductImageAdmin(nested_admin.NestedInlineModelAdmin):
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

class CollectionAdmin(nested_admin.NestedInlineModelAdmin):
    model = Collection
    inlines = [ProductAdmin]

class CollectionProductAdmin(nested_admin.NestedModelAdmin):
    #model = CollectionProduct
    inlines = [CollectionAdmin, ProductAdmin]

admin.site.register(CollectionProduct, CollectionProductAdmin)
"""