from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewset,
    CategoryFieldViewset,
    ProductViewset,
    PriceViewset,
    PictureViewset,
    CommentViewset,
    insert_product_data
)

router = DefaultRouter()
router.register(r'category', CategoryViewset, 'categories')
router.register(r'category-field', CategoryFieldViewset, 'category-fields')
router.register(r'prices', PriceViewset, 'prices')
router.register(r'pictures', PictureViewset, 'product-pictures')
router.register(r'comments', CommentViewset, 'comments')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'insert-data', insert_product_data, name='insert-data')
]
