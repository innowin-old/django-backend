from django.conf.urls import url, include
from django.contrib.gis.geoip.prototypes import record_output
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewset,
    CategoryFieldViewset,
    ProductViewset,
    PriceViewset,
    PictureViewset,
    CommentViewset
)

router = DefaultRouter()
router.register(r'category', CategoryViewset, 'categories')
router.register(r'category-field', CategoryFieldViewset, 'category-fields')
router.register(r'prices', PriceViewset, 'prices')
router.register(r'pictures', PictureViewset, 'product-pictures')
router.register(r'comments', CommentViewset, 'comments')
router.register(r'', ProductViewset, 'products')

urlpatterns = [
    url(r'^', include(router.urls))
]
