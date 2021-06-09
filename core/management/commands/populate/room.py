from faker import Faker
import random

from room.models import Room, RoomUser
from accounts.models import User
from product.models import WholesaleProductVariant

fake = Faker()
Faker.seed(999)


def populate_room():
    room = Room.objects.create(
        name = fake.text(max_nb_chars=150),
        title = fake.text(max_nb_chars=200),
        description = fake.paragraph(nb_sentences=5),
        image = fake.image_url(),
        created_at = fake.date_time_this_month()
    )
    populate_room_users(room)
    populate_wishlist(room)


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
            for i in range(fake.random_int(min=min(users.count(), 10), max=min(users.count(), 100)))
        ]
    )


def populate_wishlist(room):
    users = User.objects.all()
    variants = WholesaleProductVariant.objects.all()
    RoomWishlistProduct.objects.bulk_create(
        [
            RoomWishlistProduct(
                room = room,
                user = users[fake.random_int(min=min(users.count(), 10), max=min(users.count(), 100))],
                added_at = fake.date_time_this_month(),
                votes = fake.random_int(max=100),
                wholesale_variant = variants[i]
            ) for i in random.sample(range(0, variants.count(), fake.random_int(min=min(variants.count(), 2), max=min(users.count(), 10))))
        ]
    )