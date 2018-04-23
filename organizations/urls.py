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
    CustomerViewset,
    MetaDataViewSet
)

router = DefaultRouter()
router.register(r'meta-data', MetaDataViewSet, 'meta-data')
router.register(r'staff-counts', StaffCountViewset, 'staff-counts')
router.register(r'pictures', OrganizationPictureViewset, 'organization-pictures')
router.register(r'staff', StaffViewset, 'staffs')
router.register(r'followers', FollowViewset, 'followers')
router.register(r'abilities', AbilityViewset, 'abilities')
router.register(r'confirmations', ConfirmationViewset, 'confirmations')
router.register(r'customers', CustomerViewset, 'customers')
router.register(r'', OrganizationViewset, 'organizations')

urlpatterns = [
    url(r'^', include(router.urls))
]
