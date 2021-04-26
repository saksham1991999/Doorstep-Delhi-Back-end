from django.test import TestCase
from accounts.models import User, Address


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(id=4)

    def test_text_content(self):
        post = User.objects.get(id=4)
        expected_object_name = f'{post.id}'
        self.assertEqual(expected_object_name, '4')


class AddressTestCase(TestCase):
    def setUp(self):
        user = User.objects.create()
        Address.objects.create(user=user, full_name="FULL NAME", street_address_1="STREET ADDRESS 1", street_address_2="STREET ADDRESS 2",city="CITY",
        state="STATE", postal_code=400052, country_area="AREA", phone="982883" )

    def test_text_content(self):
        post = Address.objects.get(id=1)
        expected_object_name = f'{post.city}'
        self.assertEquals(expected_object_name, 'CITY')