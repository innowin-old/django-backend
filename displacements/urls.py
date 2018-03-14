from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import GetUserDataViewset

router = DefaultRouter()

router.register(r'users-data', GetUserDataViewset, 'users-data')

urlpatterns = [
    url('^', include(router.urls))
]