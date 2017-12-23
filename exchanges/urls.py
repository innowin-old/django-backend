from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import ExchangeViewSet, ExchangeIdentityViewSet

router = DefaultRouter()

router.register(r'identities', ExchangeIdentityViewSet)
router.register(r'', ExchangeViewSet)

urlpatterns = [
    url('^', include(router.urls))
]