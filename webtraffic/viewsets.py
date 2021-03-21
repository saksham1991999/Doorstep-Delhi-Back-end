from rest_framework import viewsets
from .models import Website
from .serializers import WebsiteSerializer
from .permissions import *
from rest_framework import permissions
from django.db.models import Q

#  Displays all websites made by the same user
class PersonalWebsiteViewset(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]
    serializer_class = WebsiteSerializer

    def get_queryset(self):
        queryset = Website.objects.filter(user = self.request.user.id)
        return queryset

#  Display all websites apart from the ones made by the same user
class GeneralWebsiteViewset(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]
    serializer_class = WebsiteSerializer

    def get_queryset(self):
        queryset = Website.objects.filter(~Q(user = self.request.user.id))
        return queryset
