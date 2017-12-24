from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import FormViewSet, GroupViewSet, FormGroupViewSet, ElementViewSet, FormGroupElementViewSet, DataViewSet


router = DefaultRouter()

router.register(r'groups', GroupViewSet)
router.register(r'form-groups', FormGroupViewSet)
router.register(r'elements', ElementViewSet)
router.register(r'form-group-elements', FormGroupElementViewSet)
router.register(r'data', DataViewSet)
router.register(r'', FormViewSet)

urlpatterns = [
    url('^', include(router.urls))
]