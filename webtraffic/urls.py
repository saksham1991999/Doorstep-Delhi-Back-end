from django.urls import path, include
from .viewsets import *
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'personal_websites', PersonalWebsiteViewset, basename='Personal_Websites')
router.register(r'general_websites', GeneralWebsiteViewset, basename='General_Websites')



website_list = GeneralWebsiteViewset.as_view({
    'get': 'list',
    'post': 'create'
})
website_detail = GeneralWebsiteViewset.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
urlpatterns = [
    path('', include(router.urls)),

]