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

# VARIANT IMAGE MODEL


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
        #ProductVariantInline,
        WholesaleProductVariantInline,
        ProductImageInline,
        ProductReviewInline,
    ]
    extra = 0


class ProductAdmin(nested_admin.NestedModelAdmin):
    inlines = [
        # ProductVariantInline,
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
