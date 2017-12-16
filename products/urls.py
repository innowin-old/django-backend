from django.conf.urls import url, include
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
router.register(r'category', CategoryViewset)
router.register(r'category-field', CategoryFieldViewset)
router.register(r'prices', PriceViewset)
router.register(r'pictures', PictureViewset)
router.register(r'comments', CommentViewset)

urlpatterns = [
    url(r'^', include(router.urls))
]
