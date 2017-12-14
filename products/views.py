from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from .models import (
        Category,
        CategoryField,
        Product,
        Price,
        Picture,
        Comment
    )

from .serializers import (
        CategorySerializer,
        CategoryFieldSerializer,
        ProductSerializer,
        PriceSerializer,
        PictureSerializer,
        CommentSerializer
    )


class CategoryViewset(ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        return CategorySerializer


class CategoryFieldViewset(ModelViewSet):
    queryset = CategoryField.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        return CategoryFieldSerializer


class ProductViewset(ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        return ProductSerializer


class PriceViewset(ModelViewSet):
    queryset = Price.objects.all()
    permisison_classes = [AllowAny]

    def get_serializer_class(self):
        return PriceSerializer


class PictureViewset(ModelViewSet):
    queryset = Picture.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        return PictureSerializer


class CommentViewset(ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        return CommentSerializer
