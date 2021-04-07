from django.contrib import admin
from .models import Wishlist, WishlistItem

import nested_admin


class WishlistItemInline(nested_admin.NestedTabularInline):
    model = WishlistItem


class WishlistAdmin(nested_admin.NestedModelAdmin):
    inline = [WishlistItemInline]


admin.site.register(Wishlist, WishlistAdmin)