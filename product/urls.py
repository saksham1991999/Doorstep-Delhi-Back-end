from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product.views import ProductAPIViewSet, CategoryViewset, ProductTypeViewset, VariationViewset, ProductViewset, CustomizationViewset

router = DefaultRouter()
router.register("products", ProductAPIViewSet, basename="products")
router.register("categories", CategoryViewset, basename="categories")
router.register("product_types", ProductTypeViewset, basename="product_type")
router.register("variants", VariationViewset, basename="variants")
router.register("products", ProductViewset, basename="products")
router.register("customization", CustomizationViewset, basename = "customizations")

urlpatterns = [
    path("", include(router.urls)),
]
