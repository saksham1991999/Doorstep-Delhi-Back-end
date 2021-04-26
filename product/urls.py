from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product.views import (
    ProductViewSet,
    CategoryViewSet,
    ProductTypeViewSet,
    VariationViewSet,
    CustomizationViewSet,
    ProductImageViewSet,
    CollectionViewSet,
    ProductVariantViewSet,
    WholesaleProductVariantViewSet
)

router = DefaultRouter()
router.register("products", ProductViewSet, basename="product-detail")
router.register("categories", CategoryViewSet, basename="category-detail")
router.register("product_types", ProductTypeViewSet, basename="product_type-detail")
router.register("variations", VariationViewSet, basename="variation-detail")
router.register("customizations", CustomizationViewSet, basename = "customization-detail")
router.register("product_image", ProductImageViewSet, basename="product_image-detail")
router.register("collection", CollectionViewSet, basename="collection-detail")
router.register("product_variants", ProductVariantViewSet, basename="product_variant-detail")
router.register("wholesale_product_variants", WholesaleProductVariantViewSet, basename="wholesale_product_variant-detail")

urlpatterns = [
    path("", include(router.urls)),
]
