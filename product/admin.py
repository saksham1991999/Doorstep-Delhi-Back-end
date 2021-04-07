from django.contrib import admin
<<<<<<< HEAD
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
=======
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
    ProductReview,
    ProductReviewFile,
    CollectionProduct,
    Collection,
)


class CollectionAdmin(nested_admin.NestedModelAdmin):
    list_display = [
                    'name',
                    ]
    list_display_links = [
                    'name',
                    ]
    search_fields = [
                    'name',
                    'description',
                    ]


class ProductReviewFileInline(nested_admin.NestedTabularInline):
    model = ProductReviewFile
    extra = 0


class ProductReviewInline(nested_admin.NestedTabularInline):
    model = ProductReview
    inlines = [ProductReviewFileInline]
    extra = 0


class ProductImageInline(nested_admin.NestedTabularInline):
    model = ProductImage
    extra = 0


class VariantImageInline(nested_admin.NestedTabularInline):
    model = VariantImage
    extra = 0


class WholesaleVariantImageInline(nested_admin.NestedTabularInline):
    model = WholesaleVariantImage
    extra = 0


class WholesaleProductVariantInline(nested_admin.NestedTabularInline):
    model = WholesaleProductVariant
    inlines = [WholesaleVariantImageInline]
    extra = 0


class ProductVariantInline(nested_admin.NestedTabularInline):
    model = ProductVariant
    inlines = [VariantImageInline]
    extra = 0


class ProductInline(nested_admin.NestedTabularInline):
    model = Product
    inlines = [
        ProductVariantInline,
        WholesaleProductVariantInline,
        ProductImageInline,
        ProductReviewInline,
    ]
    extra = 0


class ProductAdmin(nested_admin.NestedModelAdmin):
    inlines = [
        ProductVariantInline,
        WholesaleProductVariantInline,
        ProductImageInline,
        ProductReviewInline,
    ]
    list_display = [
        'category',
        'name',
    ]
    list_display_links = [
        'category',
        'name',
    ]
    search_fields = [
        'name',
    ]
    list_filter = [
                    'category',
                    ]


class CategoryAdmin(nested_admin.NestedModelAdmin):
    inlines = [ProductInline]
    list_display = [
                    'name',
                    ]
    list_display_links = [
                    'name',
                    ]
    search_fields = [
                    'name',
                    ]



class ProductTypeAdmin(nested_admin.NestedModelAdmin):
    inlines = [ProductInline]
    list_display = [
                    'name',
                    'has_variants',
                    'is_shipping_required',
                    'is_wholesale_product',
                    'qty_type',
                    'tax_percentage',
                    ]
    list_editable = [
                    'is_wholesale_product',
                    'qty_type',
                    'tax_percentage',
                    ]
    list_display_links = [
                    'name',
                    ]
    list_filter = [
                    'has_variants',
                    'is_shipping_required',
                    'is_digital',
                    'is_wholesale_product',
                    'qty_type',
                    'tax_percentage',
                    ]
    search_fields = [
                    'name',
                    'qty_type',
                    ]


class VariationAdmin(nested_admin.NestedModelAdmin):
    list_display = [
                    'name',
                    ]
    list_display_links = [
                    'name',
                    ]
    search_fields = [
                    'name',
                    ]


class CustomizationAdmin(nested_admin.NestedModelAdmin):
    list_display = [
                    'name',
                    ]
    list_display_links = [
                    'name',
                    ]
    search_fields = [
                    'name',
                    'description',
                    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Customization, CustomizationAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Collection, CollectionAdmin)
>>>>>>> 4f3ae586f40b52b5a2cb4f462a8f75ff579f07d8
