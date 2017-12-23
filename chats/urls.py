from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import MessageViewSet

router = DefaultRouter()

router.register(r'', MessageViewSet)

urlpatterns = [
    url('^', include(router.urls))
]