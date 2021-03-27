from django.urls import path, include
<<<<<<< HEAD
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

=======
from rest_framework.routers import DefaultRouter

from webtraffic.views import WebsiteAPIViewSet


app_name = 'webtraffic'


router = DefaultRouter()
router.register('websites', WebsiteAPIViewSet, basename='website')

urlpatterns = [
    path('', include(router.urls)),
>>>>>>> 4d14e6a2e2de577beb52a1de5a8e03347ab78c5d
]