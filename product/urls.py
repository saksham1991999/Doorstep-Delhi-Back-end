from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product.views import ProductAPIViewSet, CategoryViewset, ProductTypeViewset, VariationViewset, ProductViewset, CustomizationViewset
from product.views import ProductImageViewset, VariantImageViewset, WholesaleVariantImageViewset, CollectionProductViewset, CollectionViewset
from product.views import ProductVariantViewset

router = DefaultRouter()
router.register("products", ProductAPIViewSet, basename="products")
router.register("categories", CategoryViewset, basename="categories")
router.register("product_types", ProductTypeViewset, basename="product_type")
router.register("variants", VariationViewset, basename="variants")
router.register("products", ProductViewset, basename="products")
router.register("customization", CustomizationViewset, basename = "customizations")
router.register("product_image", ProductImageViewset, basename="product_image")
router.register("variant_image", VariantImageViewset, basename="variant_image")
router.register("wholesale_variant_image", WholesaleVariantImageViewset, basename="wholesale_variant_image")
router.register("collection_product", CollectionProductViewset, basename="collection_product")
router.register("collection", CollectionViewset, basename="collection")
router.register("product_variants", ProductVariantViewset, basename="product_variants")

urlpatterns = [
    path("", include(router.urls)),
]
