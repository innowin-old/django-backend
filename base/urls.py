from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import (
        BaseViewset,
        HashtagParentViewset,
        HashtagViewset,
        BaseCommentViewset
    )


router = DefaultRouter()
router.register(r'hashtag-parents', HashtagParentViewset)
router.register(r'hashtags', HashtagViewset)
router.register(r'comments', BaseCommentViewset)
router.register(r'', BaseViewset)

urlpatterns = [
    url(r'^', include(router.urls))
]
