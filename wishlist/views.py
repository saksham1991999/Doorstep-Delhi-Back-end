from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAdminUser,
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from django.db.models import Q
import datetime

from wishlist.permissions import IsOwnerOrAdmin
from wishlist.models import Wishlist
from wishlist.serializers import WishlistSerializer


class WishlistItemAPIViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        wishlists = Wishlist.objects.all()
        if not self.request.user.is_superuser:
            wishlist = get_object_or_404(Wishlist, user=self.request.user)
            return wishlist
        return wishlists
