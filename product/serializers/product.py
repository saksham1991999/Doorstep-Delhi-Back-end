from django.db.models import Q
from rest_framework import serializers
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
# from product.serializers.category import VariationSerializer


class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = ["id","name"]


class ProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    min_qty = serializers.SerializerMethodField()
    min_wholesale_price = serializers.SerializerMethodField()

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

    def get_min_wholesale_price(self, obj):
        return obj.min_wholesale_price

    def get_min_qty(self, obj):
        return obj.lowest_min_qty

    def get_image(self, obj):
        print("OBJECT:" + str(obj))
        print("TYPE:"+ str(type(obj)))
        print("\n\n\n\n\n")
        image = ProductImage.objects.filter(product=obj)[0]
        data = {
            'url': image.image.url,
            'alt': image.alt,
        }
        return data


class WholesaleProductVariantListSerializer(serializers.ModelSerializer):
    variant = VariationSerializer()
    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = WholesaleProductVariant
        fields = [
            "id",
            "name",
            "variant",
            "image",
            "min_qty",
            "per_item_qty",
            "pack_size",
            "price",
            "discounted_price",
        ]

    def get_image(self, obj):
        image = obj.images.all()
        if image.exists():
            image = image[0]
            return image.image.url
        else:
            return None
