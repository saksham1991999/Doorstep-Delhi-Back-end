from django.db import models
from django_measurement.models import MeasurementField
from versatileimagefield.fields import VersatileImageField


class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class ProductType(models.Model):
    name = models.CharField(max_length=250)
    has_variants = models.BooleanField(default=True)
    is_shipping_required = models.BooleanField(default=True)
    is_digital = models.BooleanField(default=False)
    is_wholesale_product = models.BooleanField(default=False)
    qty_type = models.CharField(max_length=256)
    tax_percentage = models.FloatField()

    def __str__(self) -> str:
        return self.name


class Variation(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Customization(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    product_type = models.ForeignKey(
        ProductType, related_name="products", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(auto_now=True, null=True)
    charge_taxes = models.BooleanField(default=True)
    product_qty = models.FloatField()
    default_variant = models.OneToOneField(
        "ProductVariant",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    visible_in_listings = models.BooleanField(default=False)
    variations = models.ManyToManyField("product.Variation")
    customizations = models.ManyToManyField("product.Customization")

    def __iter__(self):
        if not hasattr(self, "__variants"):
            setattr(self, "__variants", self.variants.all())
        return iter(getattr(self, "__variants"))

    def __str__(self) -> str:
        return self.name


class ProductVariant(models.Model):
    name = models.CharField(max_length=255, blank=True)
    product = models.ForeignKey(
        "product.Product", related_name="variants", on_delete=models.CASCADE
    )
    variant = models.ForeignKey(
        "product.Variation", related_name="products", on_delete=models.PROTECT
    )
    images = models.ManyToManyField("ProductImage", through="VariantImage")
    track_inventory = models.BooleanField(default=True)
    product_qty = models.FloatField()
    price = models.FloatField()
    discounted_price = models.FloatField()

    def __str__(self):
        return str(self.product) + "-" + self.name


class WholesaleProductVariant(models.Model):
    name = models.CharField(max_length=255, blank=True)
    store = models.ForeignKey("store.Store", related_name="wholesale_products", on_delete=models.CASCADE)
    product = models.ForeignKey(
        "product.Product", related_name="wholesale_variants", on_delete=models.CASCADE
    )
    variant = models.ForeignKey(
        "product.Variation", related_name="wholesale_products", on_delete=models.PROTECT
    )
    images = models.ManyToManyField("ProductImage", through="WholesaleVariantImage")
    min_qty = models.PositiveIntegerField()
    per_item_qty = models.PositiveIntegerField()
    pack_size = models.PositiveIntegerField()
    price = models.FloatField()
    discounted_price = models.FloatField()

    def __str__(self):
        return str(self.product) + "-" + self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    image = VersatileImageField(upload_to="products", ppoi_field="ppoi", blank=False)
    alt = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return str(self.product) + "-" + self.alt


class VariantImage(models.Model):
    variant = models.ForeignKey(
        "ProductVariant", related_name="variant_images", on_delete=models.CASCADE
    )
    image = models.ForeignKey(
        ProductImage, related_name="variant_images", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("variant", "image")


class WholesaleVariantImage(models.Model):
    variant = models.ForeignKey(
        "product.WholesaleProductVariant", related_name="wholesale_variant_images", on_delete=models.CASCADE
    )
    image = models.ForeignKey(
        ProductImage, related_name="wholesale_variant_images", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("variant", "image")


class ProductReview(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    review = models.TextField()


class ProductReviewFile(models.Model):
    review = models.ForeignKey("product.ProductReview", on_delete=models.CASCADE)
    file = models.FileField()


class CollectionProduct(models.Model):
    collection = models.ForeignKey(
        "Collection", related_name="collectionproduct", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="collectionproduct", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (("collection", "product"),)


class Collection(models.Model):
    name = models.CharField(max_length=250, unique=True)
    products = models.ManyToManyField(
        "product.Product",
        blank=True,
        related_name="collections",
        through=CollectionProduct,
        through_fields=("collection", "product"),
    )
    background_image = VersatileImageField(
        upload_to="collection-backgrounds", blank=True, null=True
    )
    background_image_alt = models.CharField(max_length=128, blank=True)
    description = models.TextField(blank=True, null=True)


