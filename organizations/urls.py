from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import (
    OrganizationViewset,
    StaffCountViewset,
    PictureViewset,
    PostViewset,
    StaffViewset,
    FollowViewset
)

router = DefaultRouter()
router.register(r'staff-counts', StaffCountViewset)
router.register(r'pictures', PictureViewset)
router.register(r'posts', PostViewset)
router.register(r'staff', StaffViewset)
router.register(r'followers', FollowViewset)
router.register(r'', OrganizationViewset)

urlpatterns = [
    url(r'^', include(router.urls))
]
