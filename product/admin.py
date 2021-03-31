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
admin.site.register(Customization)
# admin.site.register(ProductType)

#  PRODUCT MODEL
class ProductAdmin(NestedStackedInline):
    model = Product


class ProductTypeAdmin(NestedModelAdmin):
    inlines = [ProductAdmin]


admin.site.register(ProductType, ProductTypeAdmin)


class CategoryAdmin(NestedModelAdmin):
    inlines = [ProductAdmin]


admin.site.register(Category, CategoryAdmin)


class ProductVariantAdmin(NestedModelAdmin):
    inlines = [ProductAdmin]


admin.site.register(ProductVariant, ProductVariantAdmin)


##  PRODUCT VARIANT MODEL
class ProductVariantAdmin(NestedStackedInline):
    model = ProductVariant


# WHOLESALE PRODUCT VARIANT MODEL
class WholesaleProductVariantAdmin(NestedStackedInline):
    model = WholesaleProductVariant


class VariationAdmin(NestedModelAdmin):
    inlines = [ProductVariantAdmin, WholesaleProductVariantAdmin]


admin.site.register(Variation, VariationAdmin)

# PRODUCT IMAGE MODEL
class ProductImageAdmin(NestedStackedInline):
    model = ProductImage


# VARIANT IMAGE MODEL


class VariantImageAdmin(NestedStackedInline):
    model = VariantImage


""" UNABLE TO PUT PRODUCT VARIANT HERE  """
"""
class ProductVariantAdmin2(NestedModelAdmin):
    inlines = [VariantImageAdmin]
admin.site.register(ProductVariant, ProductVariantAdmin2)
"""


class WholesaleVariantImageAdmin(NestedStackedInline):
    model = WholesaleVariantImage


class WholesaleProductVariantAdmin2(NestedModelAdmin):
    inlines = [WholesaleVariantImageAdmin]


admin.site.register(WholesaleProductVariant, WholesaleProductVariantAdmin2)


class ProductImageAdmin2(NestedModelAdmin):
    inlines = [VariantImageAdmin, WholesaleVariantImageAdmin]


admin.site.register(ProductImage, ProductImageAdmin2)


# COLLECTIONPRODUCT MODEL
class CollectionProductAdmin(NestedStackedInline):
    model = CollectionProduct


class CollectionAdmin(NestedModelAdmin):
    inlines = [CollectionProductAdmin]


admin.site.register(Collection, CollectionAdmin)


class ProductAdmin2(NestedModelAdmin):
    inlines = [WholesaleProductVariantAdmin, ProductImageAdmin, CollectionProductAdmin]


admin.site.register(Product, ProductAdmin2)
