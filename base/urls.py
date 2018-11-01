from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import (
        BaseViewset,
        HashtagParentViewset,
        HashtagViewset,
        BaseCommentViewset,
        PostViewSet,
        RollViewSet,
        RollPermissionViewSet,
        HashtagRelationViewset,
        BaseCountryViewSet,
        BaseProvinceViewSet,
        BaseTownViewSet,
        BadgeCategoryViewSet,
        BadgeViewSet,
        CertificateViewSet,
        FavoriteViewSet, FavoriteBaseViewSet)


router = DefaultRouter()

router.register(r'certificates', CertificateViewSet, 'Certificates')
router.register(r'badges', BadgeViewSet, 'Badges')
router.register(r'badge-categories', BadgeCategoryViewSet, 'Badge Categories')
router.register(r'towns', BaseTownViewSet, 'Towns')
router.register(r'provinces', BaseProvinceViewSet, 'Provinces')
router.register(r'countries', BaseCountryViewSet, 'Countries')
router.register(r'hashtag-relations', HashtagRelationViewset, 'Hashtag Relations')
router.register(r'rolls', RollViewSet, 'Rolls')
router.register(r'rolls-permissions', RollPermissionViewSet, 'Permissions')
router.register(r'hashtag-parents', HashtagParentViewset, 'Hashtag Parents')
router.register(r'hashtags', HashtagViewset, 'Hashtag')
router.register(r'comments', BaseCommentViewset, 'Comments')
router.register(r'posts', PostViewSet, 'posts')
router.register(r'favorites', FavoriteViewSet, 'Favorite')
router.register(r'favorites-relations', FavoriteBaseViewSet, 'Favorite Relations')
router.register(r'', BaseViewset, 'Base')

urlpatterns = [
    url(r'^', include(router.urls))
]
