from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "name",
        ]


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = [
            "name",
            "has_variants",
            "is_shipping_required",
            "is_digital",
            "is_wholesale_product",
            "qty_type",
            "tax_percentage",
        ]


class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = ["name"]


class CustomizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customization
        fields = ["name", "description"]


class ProductSerializer(serializers.ModelSerializer):
    product_type = ProductTypeSerializer()
    category = CategorySerializer()
    variations = VariationSerializer()
    customization = CustomizationSerializer()

    class Meta:
        model = Product
        fields = [
            "product_type",
            "name",
            "description",
            "category",
            "updated_at",
            "charge_taxes",
            "product_qty",
            "default_variant",
            "visible_in_listings",
            "variations",
            "customization",
        ]


class ProductImageSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ProductImage
        fields = [
            "product",
            "image",
            "alt",
        ]


class ProductVariantSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    variant = VariationSerializer()
    images = ProductImageSerializer()

    class Meta:
        model = ProductVariant
        fields = [
            "name",
            "product",
            "variant",
            "images",
            "track_inventory",
            "product_qty",
            "price",
            "discounted_price",
        ]


class VariantImageSerializer(serializers.ModelSerializer):
    variant = ProductVariantSerializer()
    image = ProductImageSerializer()

    class Meta:
        model = VariantImage
        fields = [
            "variant",
            "image",
        ]


class WholesalePrroductVariantSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    ###store = StoreSerializer()
    variant = VariationSerializer()
    images = ProductImageSerializer()

    class Meta:
        model = WholesaleProductVariant
        fields = [
            "name",
            "store",
            "product",
            "variant",
            "images",
            "min_qty",
            "per_item_qty",
            "pack_size",
            "price",
            "discounted_price",
        ]


class WholesaleVariantImageSerializer(serializers.ModelSerializer):
    variant = WholesaleProductVariantSerializer()
    image = ProductImageSerializer()

    class Meta:
        model = WholesaleVariantImage
        fields = [
            "variant",
            "image",
        ]


class CollectionSerializer(serializers.ModelSerializer):
    products = ProductSerializer()

    class Meta:
        model = Collection
        fields = [
            "name",
            "products",
            "background_image",
            "background_image_alt",
            "description",
        ]


class CollectionProductSerializer(serializers.ModelSerializer):
    collection = CollectionSerializer()
    product = ProductSerializer()

    class Meta:
        model = CollectionProduct
        fields = [
            "collection",
            "product",
        ]
