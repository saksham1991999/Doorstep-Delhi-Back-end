from django.shortcuts import render
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

from product.serializers import * #""" NEED TO CHANGE ASAP """
# Create your views here.


class ProductAPIViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = []

    def get_queryset(self):
        products = Product.objects.all()
