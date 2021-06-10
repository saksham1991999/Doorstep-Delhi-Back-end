from faker import Faker
import random

from room.models import Room, RoomUser
from accounts.models import User , Address
from product.models import Product, WholesaleProductVariant
from room.models import *
from shop.choices import order_status_choices
from store.models import ShippingMethod
fake = Faker()
Faker.seed(999)

def populate(n):
    populate_room(n)

def populate_room(n):
    for i in range(n):
        room = Room.objects.create(
        name = fake.text(max_nb_chars=20),
        title = fake.text(max_nb_chars=200),
        description = fake.paragraph(nb_sentences=5),
        image = fake.image_url(),
        created_at = fake.date_time_this_month()
    )
        populate_room_users(room)
        populate_room_order(room)


def populate_room_users(room):
    users = User.objects.all()
    RoomUser.objects.bulk_create(
        [
            RoomUser(
                room=room,
                user=users[i],
                role=fake.random_element(elements=('A', 'U')),
                joined_at=fake.date_time_this_month()
            )
            for i in range(fake.random_int(min=min(1,users.count()), max=min(10,users.count())))
        ]
    )
    populate_room_wishlist_product(room)


def populate_room_wishlist_product(room):
    users = room.users.all()
    variants = WholesaleProductVariant.objects.all()
    
    RoomWishlistProduct.objects.bulk_create(
    [
            RoomWishlistProduct(
                room = room,
                user = users[fake.random_int(min=min(1,users.count()-1), max=min(100,users.count()-1))],
                added_at = fake.date_time_this_month(),
                votes = fake.random_int(max = users.count()),
                wholesale_variant = variants[i]
            )
            
            for i in range(fake.random_int(min=min(variants.count(), 1), max=min(variants.count(), 100)))
                
        ]
    )   
    populate_wishlist_product_vote(room) 
    

def populate_wishlist_product_vote(room):
    users = room.users.all()
    products = RoomWishlistProduct.objects.filter( room = room)
    for i in range(products.count()):
        WishlistProductVote.objects.bulk_create(
        [   
            WishlistProductVote(
            product = products[i],
            user = users[j]
            )
            for j in random.sample(range(0,users.count()),products[i].votes)
        ]

    )

def populate_room_order(room):
    bill_add = Address.objects.all()
    ship_add = Address.objects.all()
    ship_method = ShippingMethod.objects.all()
    RoomOrder.objects.bulk_create(
        [
            RoomOrder(
                room = room,
                created = fake.date_time_this_month(),
                status = fake.random_choices(order_status_choices, length=1),
                tracking_client_id = fake.text(max_nb_chars=100),
                billing_address = bill_add[random.randint(0,bill_add.count())],
                shipping_address = ship_add[random.randint(0,ship_add.count())],
                shipping_method = ship_method[random.randint(0,ship_method.count()-1)],
                shipping_price = fake.random_int(max=1000),
                total_net_amount = fake.random_int(max=1000),
                undiscounted_total_net_amount = fake.random_int(max=1000)
            )
        ]
    )
