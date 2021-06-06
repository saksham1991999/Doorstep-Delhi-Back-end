from room.serializers import RoomOrderLineSerializer
from django.contrib import admin
from room.models import Message, Room, RoomUser,RoomWishlistProduct,WishlistProductVote,RoomOrder, RoomOrderLine, UserOrderLine, OrderEvent,Invoice, Message

# Register your models here.
admin.site.register(Room)
admin.site.register(RoomUser)
admin.site.register(RoomWishlistProduct)
admin.site.register(WishlistProductVote)
admin.site.register(RoomOrder)
admin.site.register(RoomOrderLine)
admin.site.register(UserOrderLine)
admin.site.register(OrderEvent)
admin.site.register(Invoice)
admin.site.register(Message)