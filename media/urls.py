from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import MediaViewSet

router = DefaultRouter()

router.register(r'', MediaViewSet, 'medias')

urlpatterns = [
    url('^', include(router.urls))
]
