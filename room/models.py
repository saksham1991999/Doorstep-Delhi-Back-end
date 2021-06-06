from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save

from shop.choices import order_status_choices, order_event_type_choices, voucher_type_choices, discout_value_type_choices


class Room(models.Model):
    name = models.CharField(max_length=150)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)


user_role_choices = (
    ("A", "Admin"),
    ("U", "User"),
)


class RoomUser(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    room = models.ForeignKey("room.Room", on_delete=models.CASCADE)
    role = models.CharField(max_length=2, choices=user_role_choices)
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'room')


class RoomWishlistProduct(models.Model):
    room = models.ForeignKey('room.Room', on_delete=models.CASCADE)
    wholesale_variant = models.ForeignKey('product.WholesaleProductVariant', on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    votes = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ("room", "wholesale_variant")


class WishlistProductVote(models.Model):
    product = models.ForeignKey('room.RoomWishlistProduct', on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)

    class Meta:
        unique_together = ("product", "user")


class RoomOrder(models.Model):
    room = models.ForeignKey("room.Room", on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(default=now, editable=False)
    status = models.CharField(
        max_length=32, default="unfulfilled", choices=order_status_choices)
    tracking_client_id = models.CharField(max_length=36, blank=True, editable=False)
    billing_address = models.ForeignKey(
        "accounts.Address", related_name="+", editable=False, null=True, on_delete=models.SET_NULL
    )
    shipping_address = models.ForeignKey(
        "accounts.Address", related_name="+", editable=False, null=True, on_delete=models.SET_NULL
    )
    pickup_point = models.ForeignKey(
        'store.PickupPoint', related_name="pickup_point", null=True, on_delete=models.SET_NULL
    )
    shipping_method = models.ForeignKey(
        "store.ShippingMethod",
        blank=True,
        null=True,
        related_name="shipping_method",
        on_delete=models.SET_NULL,
    )
    shipping_price = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
        editable=False,
    )
    total_net_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    undiscounted_total_net_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )


class RoomOrderLine(models.Model):
    order = models.ForeignKey(
        'room.RoomOrder', related_name="lines", editable=False, on_delete=models.CASCADE, null=True
    )
    variant = models.ForeignKey(
        "product.WholesaleProductVariant",
        related_name="order_line_wholesale_product_variant",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)


class UserOrderLine(models.Model):
    product = models.ForeignKey('room.RoomOrderLine', related_name='users_quatity',on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    quantity_fulfilled = models.IntegerField(
        validators=[MinValueValidator(0)], default=0
    )
    updated_at = models.DateTimeField(auto_now=True)


class OrderEvent(models.Model):
    date = models.DateTimeField(default=now, editable=False)
    type = models.CharField(
        max_length=255,
        choices=[
            (type_name.upper(), type_name) for type_name, _ in order_event_type_choices
        ],
    )
    order = models.ForeignKey("room.RoomOrder", related_name="events", on_delete=models.CASCADE)
    user = models.ForeignKey(
        "accounts.User",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )


class Invoice(models.Model):
    order = models.ForeignKey(
        "room.RoomOrder", related_name="invoices", null=True, on_delete=models.SET_NULL
    )
    number = models.CharField(max_length=255, null=True)
    created = models.DateTimeField(null=True)
    external_url = models.URLField(null=True, max_length=2048)
    invoice_file = models.FileField(upload_to="invoices")

class Message(models.Model):
    file_field = models.FileField(upload_to='media/Message', blank=True)
    message_text = models.CharField(max_length=1000, blank=True)
    user = models.ForeignKey('room.RoomUser', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey('room.Room', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__() +" : "+ self.message_text