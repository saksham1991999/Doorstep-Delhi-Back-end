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
from wishlist.permissions import IsAdminOrReadOnly

from wishlist.models import Wishlist, WishlistItem
from wishlist.serializers import WishlistSerializer, WishlistItemSerializer

# Create your views here.


class WishlistItemAPIViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistItemSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        wishlist_items = WishlistItem.objects.all()
        return wishlist_items
