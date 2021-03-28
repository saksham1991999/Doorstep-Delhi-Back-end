from django.contrib import admin
from product.models import Category, ProductType, Variation, Customization, Product, ProductVariant, WholesaleProductVariant, ProductImage, VariantImage, WholesaleVariantImage, CollectionProduct, Collection


# Register your models here.

admin.site.register(Category)
admin.site.register(ProductType)
admin.site.register(Variation)
admin.site.register(Customization)
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(WholesaleProductVariant)
admin.site.register(ProductImage)
admin.site.register(VariantImage)
admin.site.register(WholesaleVariantImage)
admin.site.register(CollectionProduct)
admin.site.register(Collection)