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

    def get_queryset(self):
        queryset = Category.objects.all()

        parent = self.request.query_params.get('parent', None)
        if parent is not None:
            queryset = queryset.filter(parent_id=parent)

        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title=title)

        return queryset

    def get_serializer_class(self):
        return CategorySerializer


class CategoryFieldViewset(ModelViewSet):
    queryset = CategoryField.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = CategoryField.objects.all()

        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category_id=category)

        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title=title)

        return queryset

    def get_serializer_class(self):
        return CategoryFieldSerializer


class ProductViewset(ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Product.objects.all()

        owner = self.request.query_params.get('owner', None)
        if owner is not None:
            queryset = queryset.filter(owner_id=owner)

        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category_id=category)

        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)

        country = self.request.query_params.get('country', None)
        if country is not None:
            queryset = queryset.filter(country=country)

        province = self.request.query_params.get('province', None)
        if province is not None:
            queryset = queryset.filter(province=province)

        city = self.request.query_params.get('city', None)
        if city is not None:
            queryset = queryset.filter(city=city)

        description = self.request.query_params.get('description')
        if description is not None:
            queryset = queryset.filter(description=description)

        return queryset

    def get_serializer_class(self):
        return ProductSerializer


class PriceViewset(ModelViewSet):
    queryset = Price.objects.all()
    permisison_classes = [AllowAny]

    def get_queryset(self):
        queryset = Price.objects.all()

        product = self.request.query_params.get('product', None)
        if product is not None:
            queryset = queryset.filter(product_id=product)

        return queryset

    def get_serializer_class(self):
        return PriceSerializer


class PictureViewset(ModelViewSet):
    queryset = Picture.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Picture.objects.all()

        product = self.request.query_params.get('product', None)
        if product is not None:
            queryset = queryset.filter(product_id=product)

        description = self.request.query_params.get('description', None)
        if description is not None:
            queryset = queryset.filter(description=description)

        return queryset

    def get_serializer_class(self):
        return PictureSerializer


class CommentViewset(ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Comment.objects.all()

        product = self.request.query_params.get('product', None)
        if product is not None:
            queryset = queryset.filter(product_id=product)

        user = self.request.query_params.get('user', None)
        if user is not None:
            queryset = queryset.filter(user_id=user)

        text = self.request.query_params.get('text', None)
        if text is not None:
            queryset = queryset.filter(text=text)

        return queryset

    def get_serializer_class(self):
        return CommentSerializer
