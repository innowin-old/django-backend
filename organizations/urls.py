from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import (
    OrganizationViewset,
    StaffCountViewset,
    OrganizationPictureViewset,
    PostViewset,
    StaffViewset,
    FollowViewset,
    AbilityViewset,
    ConfirmationViewset,
    CustomerViewset
)

router = DefaultRouter()
router.register(r'staff-counts', StaffCountViewset, 'Staff Counts')
router.register(r'pictures', OrganizationPictureViewset, 'Pictures')
router.register(r'posts', PostViewset, 'Posts')
router.register(r'staff', StaffViewset, 'Staff')
router.register(r'followers', FollowViewset, 'Followers')
router.register(r'abilities', AbilityViewset, 'Abilities')
router.register(r'confirmations', ConfirmationViewset, 'Confirmations')
router.register(r'customers', CustomerViewset, 'Customers')
router.register(r'', OrganizationViewset, 'Organizations')

urlpatterns = [
    url(r'^', include(router.urls))
]
