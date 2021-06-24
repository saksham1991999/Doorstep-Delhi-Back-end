from django.conf import settings
from django.core.checks import messages
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import ClientLog,Support,SupportCategory,SupportReply,SupportSubCategory
from .serializers import SupportSerializer,ClientLogSerializer,SupportCategorySerializer,SupportSubCategorySerilizer,SupportReplySerializer

# Create your views here.

class SupportViewSet(viewsets.ModelViewSet):
    
    
    def get_queryset(self,request):
        queryset = Support.objects.filter(self.request.user)
        serializer_class = SupportSerializer(queryset,many=True)
        return serializer_class.data
    




class SupportReplyViewSet(viewsets.ModelViewSet):
     
     serializer_class = SupportReplySerializer()
     def get_queryset(self,request):
         query_set = SupportReply.objects.filter(user=self.request.user)
         Serializer_class=SupportReplySerializer(query_set)
         return Serializer_class.data
     

     @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated,])
     def update(self, request, pk, *args, **kwargs):
        try:
            message = self.get_object()
            user = request.user
            file = request.data["file"]
            SupportReply =SupportReply.objects.create(
                message=message, user=user, type=type
            )
            return Response("Done", status=status.HTTP_200_OK)
        except:
            return Response("Error", status=status.HTTP_400_BAD_REQUEST)

    


