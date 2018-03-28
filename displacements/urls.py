from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import GetUserDataViewset, GetProductDataViewset

router = DefaultRouter()

router.register(r'users-data', GetUserDataViewset, 'users-data')
router.register(r'products-data', GetProductDataViewset, 'products-data')

urlpatterns = [
    url('^', include(router.urls))
]