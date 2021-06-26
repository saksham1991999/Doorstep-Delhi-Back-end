from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from product.models import (
    Category,
    SubCategory,
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
    ProductReview,
    ProductReviewFile,
    Brand
)
from store.serializers import StoreSerializer


class ProductListSerilaizer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    min_qty = serializers.SerializerMethodField()
    # min_wholesale_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "average_rating",
            "image",
            "min_qty",
            "min_wholesale_price",
        ]

    # def get_min_wholesale_price(self, obj):


    def get_min_qty(self, obj):
        return obj.lowest_min_qty

    def get_image(self, obj):
        image = ProductImage.objects.filter(product=obj)[0]
        data = {
            'url': image.image.url,
            'alt': image.alt,
        }
        return data

    
        
    # def get_product_variants(self, obj):
    #     serializer = ProductVariantSerializer(ProductVariant.objects.filter(product=obj), many=True)
    #     return serializer.data

    def get_variant_images(self, obj):
        images = ProductImage.objects.values_list('image', flat=True)
        return images


class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = [
            "id",
            "name",
        ]


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "icon",
            "sub_categories",
        ]

    def get_sub_categories(self, obj):
        sub_categories = SubCategory.objects.filter(category=obj)
        serializer = SubCategorySerializer(sub_categories, many=True)
        return serializer.data


class ProductTypeSerializer(serializers.ModelSerializer):
    # products = serializers.SerializerMethodField(read_only=True)

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

    def get_products(self, obj):
        products = Product.objects.filter(category=obj)
        serializer = ProductListSerilaizer(products, many=True)
        return serializer.data


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
    customization = CustomizationSerializer()

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


class ProductImageSerializer(serializers.ModelSerializer):
    product = ProductListSerilaizer(many = True)
    class Meta:
        model = ProductImage
        fields = [
            "id",
            "product",
            "image",
            "alt",
        ]


class ProductVariantSerializer(serializers.ModelSerializer):
    variant = VariationSerializer()
    images = ProductImageSerializer(many =True)

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


class WholesaleProductVariantSerializer(serializers.ModelSerializer):
    store = StoreSerializer()
    variant = VariationSerializer()
    images = ProductImageSerializer(many = True)

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



class ProductReviewSerializer(serializers.ModelSerializer):
    files = serializers.ModelSerializer(read_only=True)

    class Meta:
        model = ProductReview
        fields = [
            "user",
            "product",
            "rating",
            "review",
            'files',
        ]

    def get_files(self, obj):
        files = ProductReviewFile.objects.filter(review = obj).values_list("file.url", flat=True)
        return files


class ProductDetailSerializer(serializers.ModelSerializer):
    product_type = ProductTypeSerializer()
    category = CategorySerializer()
    variations = VariationSerializer()
    customization = CustomizationSerializer(read_only=True,many=True)
    variants = serializers.SerializerMethodField(read_only=True)
    wholesale_variants = serializers.SerializerMethodField(read_only=True)
    reviews = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'product_type',
            'category',
            'variations',
            'customization',
            'name',
            'description',
            'updated_at',
            'charge_taxes',
            'product_qty',
            'visible_in_listings',
            'variants',
            'wholesale_variants',
            'reviews',
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

    def get_variants(self, obj):
        variants = ProductVariant.objects.filter(product=obj)
        serializer = ProductVariantSerializer(variants, many=True)
        return serializer.data

    def get_wholesale_variants(self, obj):
        variants = WholesaleProductVariant.objects.filter(product=obj)
        serializer = WholesaleProductVariantSerializer(variants, many=True)
        return serializer.data

    def get_reviews(self, obj):
        reviews = ProductReview.objects.filter(product=obj)
        serializer = ProductReviewSerializer(reviews, many=True)
        return serializer.data


class CollectionSerializer(serializers.ModelSerializer):
    products = ProductListSerilaizer(many = True)

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

class BrandSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Brand
        fields = ["id", "name" , "image" , "alt" , "description"]



class HomeCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name"]
