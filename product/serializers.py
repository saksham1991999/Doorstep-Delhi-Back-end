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
            "id",
            "name",
        ]


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = [
            "id",
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
        fields = ["id","name"]


class CustomizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customization
        fields = ["id","name", "description"]


class ProductSerializer(serializers.ModelSerializer):
    product_type = ProductTypeSerializer()
    category = CategorySerializer()
    variations = VariationSerializer()
    customization = CustomizationSerializer() # SHOULD BE UNCOMMENTED

    class Meta:
        model = Product
        fields = [
            "id",
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

    def create(self, validated_data):
        product_type = validated_data.pop("product_type")
        category = validated_data.pop("category")
        variations = validated_data.pop("variations")
        customization = validated_data.pop("customization")
        products = Product.objects.create(**validated_data)
        for product in products:
            Product.objects.create(
                product_type=product_type,
                category=category,
                variations=variations,
                customizations=customization,
                **product
            )
        return products


class ProductSerializer2(serializers.ModelSerializer):
    product_type = ProductTypeSerializer()
    category = CategorySerializer()
    variations = VariationSerializer()
    customization = CustomizationSerializer(read_only=True,many=True) # SHOULD BE UNCOMMENTED

    class Meta:
        model = Product
        fields = ['id','product_type','category','variations','customization','name', 'description', 'updated_at', 'charge_taxes', 'product_qty', 'visible_in_listings']

    def create(self, validated_data):
        product_type = validated_data.pop("product_type")
        category = validated_data.pop("category")
        variations = validated_data.pop("variations")
        customization = validated_data.pop("customization")
        products = Product.objects.create(**validated_data)
        for product in products:
            Product.objects.create(
                product_type=product_type,
                category=category,
                variations=variations,
                customizations=customization,
                **product
            )
        return products
    
    def get_customization(self,obj):
        serializer = CustomizationSerializer(Customization.objects.all(), many=True)
        return serializer.data

class ProductImageSerializer(serializers.ModelSerializer):
    product = ProductSerializer2()

    class Meta:
        model = ProductImage
        fields = [
            "id",
            "product",
            "image",
            "alt",
            
        ]



class ProductVariantSerializer(serializers.ModelSerializer):
    product = ProductSerializer2(many=False)
    variant = VariationSerializer()
    images = serializers.PrimaryKeyRelatedField(queryset=ProductImage.objects.all(), many=True)

    class Meta:
        model = ProductVariant
        fields = [
            "id",
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
            "id",
            "variant",
            "image",
        ]


class WholesaleProductVariantSerializer(serializers.ModelSerializer):
    product = ProductSerializer2()
    ###store = StoreSerializer()
    variant = VariationSerializer()
    images = ProductImageSerializer(many=True)

    class Meta:
        model = WholesaleProductVariant
        fields = [
            "id",
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
    variant = WholesaleProductVariantSerializer() # SHOULD BE UNCOMMENTED
    image = ProductImageSerializer()

    class Meta:
        model = WholesaleVariantImage
        fields = [
            "id",
            "variant",
            "image",
        ]


class CollectionSerializer(serializers.ModelSerializer):
    # products = ProductSerializer()        # SHOULD BE UNCOMMENTED

    class Meta:
        model = Collection
        fields = [
            "id",
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
            "id",
            "collection",
            "product",
        ]

class ProductListVariantImageSerializer(serializers.ModelSerializer):
    # variant = ProductVariantSerializer()
    # image = ProductImageSerializer()

    class Meta:
        model = VariantImage
        fields = [
            "id",
            # "variant",
            "image",
        ]



class ProductListSerilaizer(serializers.ModelSerializer):
    # product_variants = serializers.SerializerMethodField()
    variant_images = serializers.SerializerMethodField()
    # product_variant = ProductListProductVariantSerializer(many=False, read_only=True) # READ ONLY SHOULD BE FALSE
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "product_qty",
            # "product_variants",
            "variant_images"
        ]

    # def get_product_variants(self, obj):
    #     serializer = ProductVariantSerializer(ProductVariant.objects.filter(product=obj), many=True)
    #     return serializer.data

    def get_variant_images(self, obj):
        images = ProductImage.objects.values_list('image', flat=True)
        return images