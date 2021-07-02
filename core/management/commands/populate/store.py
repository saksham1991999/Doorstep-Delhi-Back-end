from faker import Faker

from store.models import BankAccount, PickupPoint, ShippingZone, Store, ShippingMethod
from accounts.models import Address

fake = Faker()
Faker.seed(999)


def populate(n):
    add_stores(10)
    add_shipping_zones(10)
    add_shipping_method(10)
    add_bank_accounts(100)
    


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
                address=addresses[fake.random_int(max=addresses_count-1)],
                logo = fake.image_url(),
                website = fake.url(),
                facebook_link = fake.url(),
                instagram_link = fake.url()
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
    
def add_bank_accounts(n):
    stores = Store.objects.all()
    BankAccount.objects.bulk_create(
        [
            BankAccount(
            store = stores[fake.random_int(max=stores.count()-1)],
            holder_name = fake.word(),
            account_number = fake.random_int(min = 11 , max = 11),
            ifsc = fake.bothify(text='????##########', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            account_type = fake.random_element(elements=("S","C")),
            bank_name = fake.text(max_nb_chars=20)
            )
            for _ in range(n)
        ]
        
    )

# def populate_pickup_point():
#     addresses = Address.objects.all()
#     PickupPoint.objects.bulk_create(
#         [
#             PickupPoint(
#                 name=fake.word(),
#                 email = fake.e
#             )
#             for _ in range(n)
#         ]
#     )