from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import ExchangeViewSet, ExchangeIdentityViewSet

router = DefaultRouter()

router.register(r'identities', ExchangeIdentityViewSet, 'identities')
router.register(r'', ExchangeViewSet, 'exchanges')

urlpatterns = [
    url('^', include(router.urls))
]