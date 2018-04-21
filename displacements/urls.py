from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import GetUserDataViewset, GetProductDataViewset, GetOrganizationDataViewSet, GetExchangeDataViwSet

router = DefaultRouter()

router.register(r'exchanges-data', GetExchangeDataViwSet, 'exchanges-data')
router.register(r'organizations-data', GetOrganizationDataViewSet, 'organizations-data')
router.register(r'products-data', GetProductDataViewset, 'products-data')
router.register(r'users-data', GetUserDataViewset, 'users-data')
router.register(r'products-data', GetProductDataViewset, 'products-data')

urlpatterns = [
    url('^', include(router.urls))
]