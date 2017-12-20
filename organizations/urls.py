from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import (
    OrganizationViewset,
    StaffCountViewset,
<<<<<<< HEAD
    PictureViewset
=======
    OrganizationPictureViewset,
    PostViewset,
    StaffViewset,
    FollowViewset,
    AbilityViewset,
    ConfirmationViewset,
    CustomerViewset
>>>>>>> saeid
)

router = DefaultRouter()
router.register(r'staff-counts', StaffCountViewset)
<<<<<<< HEAD
router.register(r'pictures', PictureViewset)
=======
router.register(r'pictures', OrganizationPictureViewset)
router.register(r'posts', PostViewset)
router.register(r'staff', StaffViewset)
router.register(r'followers', FollowViewset)
router.register(r'abilities', AbilityViewset)
router.register(r'confirmations', ConfirmationViewset)
router.register(r'customers', CustomerViewset)
>>>>>>> saeid
router.register(r'', OrganizationViewset)

urlpatterns = [
    url(r'^', include(router.urls))
]
