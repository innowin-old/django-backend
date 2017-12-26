from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import (
    OrganizationViewset,
    StaffCountViewset,
    OrganizationPictureViewset,
    StaffViewset,
    FollowViewset,
    AbilityViewset,
    ConfirmationViewset,
    CustomerViewset
)

router = DefaultRouter()
router.register(r'staff-counts', StaffCountViewset)
router.register(r'pictures', OrganizationPictureViewset)
router.register(r'staff', StaffViewset)
router.register(r'followers', FollowViewset)
router.register(r'abilities', AbilityViewset)
router.register(r'confirmations', ConfirmationViewset)
router.register(r'customers', CustomerViewset)
router.register(r'', OrganizationViewset)

urlpatterns = [
    url(r'^', include(router.urls))
]
