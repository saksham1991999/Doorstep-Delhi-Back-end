from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q
import datetime

from .serializers import WebsiteSerializer
from .models import Website, WebsiteHit
from .permissions import IsWebsiteOwner


class WebsiteAPIViewSet(viewsets.ModelViewSet):
    serializer_class = WebsiteSerializer
    permission_classes = [IsAuthenticated, IsWebsiteOwner]

    def get_queryset(self):
        websites = Website.objects.filter(user = self.request.user)

        if self.request.query_params.get('search', None):
            search = self.request.query_params.get('search', None)
            websites = websites.filter(Q(name__icontains=search) | Q(url__icontains=search))

        if self.request.query_params.get('namesort', None):
            sort = self.request.query_params.get('namesort', None)
            if sort=='asc':
                websites = websites.order_by('name')
            elif sort == 'dsc':
                websites = websites.order_by('-name')

        if self.request.query_params.get('sort', None):
            sort = self.request.query_params.get('sort', None)
            if sort=='nameasc':
                websites = websites.order_by('name')
            elif sort == 'namedsc':
                websites = websites.order_by('-name')
            elif sort == 'dateasc':
                websites = websites.order_by('created_at')
            elif sort == 'datedsc':
                websites = websites.order_by('-created_at')

        return websites

    @action(detail=False, methods=['get'])
    def surf_websites(self, request, *args, **kwargs):
        surfed_websites = WebsiteHit.objects.filter(user=request.user, created_at__lt = datetime.datetime.now() - datetime.timedelta(days=1)).values_list("website")
        websites = Website.objects.exclude(user=request.user).exclude(id__in = surfed_websites)
        serializer = WebsiteSerializer(websites, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def hit(self, request, pk, *args, **kwargs):
        try:
            website = self.get_object()
            user = request.user
            type = request.data['type']
            website_hit = WebsiteHit.objects.create(website = website, user = user, type=type)
            return Response("Done", status = status.HTTP_200_OK)
        except:
            return Response("Error", status = status.HTTP_400_BAD_REQUEST)