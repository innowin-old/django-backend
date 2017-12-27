from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import (
        BaseViewset,
        HashtagParentViewset,
        HashtagViewset,
        BaseCommentViewset,
        PostViewSet
    )


router = DefaultRouter()
<<<<<<< HEAD
router.register(r'posts', PostViewSet)
router.register(r'hashtag-parents', HashtagParentViewset)
router.register(r'hashtags', HashtagViewset)
router.register(r'comments', BaseCommentViewset)
router.register(r'', BaseViewset)
=======
router.register(r'hashtag-parents', HashtagParentViewset, 'Hashtag Parents')
router.register(r'hashtags', HashtagViewset, 'Hashtag')
router.register(r'comments', BaseCommentViewset, 'Comments')
router.register(r'', BaseViewset, 'Base')
>>>>>>> saeid

urlpatterns = [
    url(r'^', include(router.urls))
]
