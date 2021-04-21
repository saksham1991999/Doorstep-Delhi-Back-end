from django.test import TestCase
from wishlist.models import Wishlist, WishlistItem
from product.models import Product, ProductType
# Create your tests here.

class WishlistTestCase(TestCase):
    def setUp(self):
        Wishlist.objects.create(id=4)

    def test_text_content(self):
        post = Wishlist.objects.get(id=4)
        expected_object_name = f'{post.id}'
        self.assertEqual(expected_object_name, '4')

class WishlistItemTestCase(TestCase):
    def setUp(self):
        wishlist = Wishlist.objects.create(id=5)
        product_type = ProductType.objects.create(tax_percentage=4.00)
        product = Product.objects.create(name="NAME", product_qty=4, product_type=product_type)
        WishlistItem.objects.create(product = product, wishlist=wishlist)

    def test_text_content(self):
        post = WishlistItem.objects.get(id=1)
        expected_object_name = f'{post.id}'
        self.assertEquals(expected_object_name, '1')