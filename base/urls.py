from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import (
        BaseViewset,
        HashtagParentViewset,
        HashtagViewset,
        BaseCommentViewset,
        PostViewSet,
        RollViewSet,
        RollPermissionViewSet
        #CertificateViewSet
    )


router = DefaultRouter()
#router.register(r'certificates', CertificateViewSet, 'certificates')
router.register(r'rolls', RollViewSet, 'Rolls')
router.register(r'rolls-permissions', RollPermissionViewSet, 'Rolls Permissions')
router.register(r'hashtag-parents', HashtagParentViewset, 'Hashtag Parents')
router.register(r'hashtags', HashtagViewset, 'Hashtag')
router.register(r'comments', BaseCommentViewset, 'Comments')
router.register(r'posts', PostViewSet, 'posts')
router.register(r'', BaseViewset, 'Base')

urlpatterns = [
    url(r'^', include(router.urls))
]
