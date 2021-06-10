from faker import Faker

from store.models import ShippingZone, Store, ShippingMethod
from accounts.models import Address

fake = Faker()
Faker.seed(999)


def populate(n):
    add_stores(30)
    add_shipping_zones(10)
    add_shipping_method(10)


def add_shipping_zones(n):
    ShippingZone.objects.bulk_create(
        [ShippingZone(name = fake.word()) for _ in range(n)]
    )


def add_stores(n):
    addresses = Address.objects.all()
    addresses_count = addresses.count()
    Store.objects.bulk_create(
        [
            Store(
                name=fake.word(),
                email=fake.email(),
                address=addresses[fake.random_int(max=addresses_count-1)]
            )
            for _ in range(n)
        ]
    )


def add_shipping_method(n):
    shipping_zones = ShippingZone.objects.all()
    ShippingMethod.objects.bulk_create(
        [
            ShippingMethod(
                name=fake.word(),
                type=fake.random_element(elements=("S", "FS", "DS")),
                shipping_zone=shipping_zones[fake.random_int(max=shipping_zones.count()-1)],
                minimum_delivery_days=fake.random_digit(),
                maximum_delivery_days=fake.random_int(min=10)
            )
            for _ in range(n)
        ]
    )