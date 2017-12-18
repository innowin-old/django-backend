from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import (
        HashtagParentViewset,
        HashtagViewset
    )


router = DefaultRouter()
router.register(r'hashtag-parents', HashtagParentViewset)
router.register(r'hashtags', HashtagViewset)


urlpatterns = [
    url(r'^', include(router.urls))
]
