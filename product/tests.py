from django.test import TestCase, Client
import unittest

# Create your tests here.

class APITest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_details(self):
        product_response = self.client.get('/products/products/')
        product_categories = self.client.get('/products/categories/')
        product_types = self.client.get('/products/product_types/')
        variants = self.client.get('/products/variants/')
        customization = self.client.get('/products/customization/')
        product_image = self.client.get('/products/product_image/')
        variant_image = self.client.get('/products/variant_image/')
        wholesale_variant_image = self.client.get('/products/wholesale_variant_image/')
        collection = self.client.get('/products/collection/')
        collection_product = self.client.get('/products/collection_product/')
        product_variants = self.client.get('/products/product_variants/')
        wholesale_product_variants = self.client.get('/products/wholesale_product_variants/')

        self.assertEqual(product_response.status_code, 200)
        self.assertEqual(product_categories.status_code, 200)
        self.assertEqual(product_types.status_code, 200)
        self.assertEqual(variants.status_code, 200)
        self.assertEqual(customization.status_code, 200)
        self.assertEqual(product_image.status_code, 200)
        self.assertEqual(variant_image.status_code, 200)
        self.assertEqual(wholesale_variant_image.status_code, 200)
        self.assertEqual(collection.status_code, 200)
        self.assertEqual(collection_product.status_code, 200)
        self.assertEqual(product_variants.status_code, 200)
        self.assertEqual(wholesale_product_variants.status_code, 200)
# class SimpleTest(unittest.TestCase):
#     def setUp(self):
#         # Every test needs a client.
#         self.client = Client()

#     def test_details(self):
#         # Issue a GET request.
#         response = self.client.get('/customer/details/')

#         # Check that the response is 200 OK.
#         self.assertEqual(response.status_code, 200)

#         # Check that the rendered context contains 5 customers.
#         self.assertEqual(len(response.context['customers']), 5)