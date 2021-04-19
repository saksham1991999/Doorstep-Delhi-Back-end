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
    # customization = CustomizationSerializer() # SHOULD BE UNCOMMENTED

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
            # "customization",
        ]

    def create(self, validated_data):
        product_type = validated_data.pop("product_type")
        category = validated_data.pop("category")
        variations = validated_data.pop("variations")
        products = Product.objects.create(**validated_data)
        for product in products:
            Product.objects.create(
                product_type=product_type,
                category=category,
                variations=variations,
                **product
            )
        return products


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
    # images = ProductImageSerializer(many=True) # SHOULD BE UNCOMMENTED
    images = serializers.PrimaryKeyRelatedField(queryset=ProductImage.objects.all(), many=True)

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


class WholesaleProductVariantSerializer(serializers.ModelSerializer):
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
    variant = WholesaleProductVariantSerializer(many=True) # SHOULD BE UNCOMMENTED
    image = ProductImageSerializer()

    class Meta:
        model = WholesaleVariantImage
        fields = [
            "variant",
            "image",
        ]


class CollectionSerializer(serializers.ModelSerializer):
    # products = ProductSerializer()        # SHOULD BE UNCOMMENTED

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

class ProductListProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = [
            "name",
            "images",
            "product_qty",
            "price",
            "discounted_price"
        ]

class ProductListSerilaizer(serializers.ModelSerializer):
    product_variants = serializers.SerializerMethodField()
    # product_variant = ProductListProductVariantSerializer(many=False, read_only=True) # READ ONLY SHOULD BE FALSE
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "product_qty",
            "product_variants"
        ]

    def get_product_variants(self, obj):
        return [p.__str__() for p in ProductVariant.objects.filter(product=obj)]