from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import FormViewSet, GroupViewSet, FormGroupViewSet, ElementViewSet, FormGroupElementViewSet, DataViewSet


router = DefaultRouter()

router.register(r'groups', GroupViewSet, 'groups')
router.register(r'form-groups', FormGroupViewSet, 'form-groups')
router.register(r'elements', ElementViewSet, 'elements')
router.register(r'form-group-elements', FormGroupElementViewSet, 'form-group-elements')
router.register(r'data', DataViewSet, 'data')
router.register(r'', FormViewSet, 'forms')

urlpatterns = [
    url('^', include(router.urls))
]