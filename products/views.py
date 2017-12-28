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
    # queryset = Category.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Category.objects.all()

        parent_id = self.request.query_params.get('parent_id', None)
        if parent_id is not None:
            queryset = queryset.filter(category_parent_id=parent_id)

        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__contains=name)

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__contains=title)

        return queryset

    def get_serializer_class(self):
        return CategorySerializer


class CategoryFieldViewset(ModelViewSet):
    # queryset = CategoryField.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = CategoryField.objects.all()

        """
            Category Filter Options
        """
        category_id = self.request.query_params.get('category_id', None)
        if category_id is not None:
            queryset = queryset.filter(field_category_id=category_id)

        category_name = self.request.query_params.get('category_name', None)
        if category_name is not None:
            queryset = queryset.filter(field_category__name__contains=category_name)

        category_title = self.request.query_params.get('category_title', None)
        if category_title is not None:
            queryset = queryset.filter(field_category__title__contains=category_title)

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
    # queryset = Product.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Product.objects.all()

        """
            Owner Filter Options
        """
        owner_id = self.request.query_params.get('owner_id', None)
        if owner_id is not None:
            queryset = queryset.filter(product_owner_id=owner_id)

        owner_name = self.request.query_params.get('owner_name', None)
        if owner_name is not None:
            queryset = queryset.filter(product_owner__name__contains=owner_name)

        owner_username = self.request.query_params.get('owner_username', None)
        if owner_username is not None:
            queryset = queryset.filter(product_owner__identity_user__username__contains=owner_username)

        """
            Category Filter Options
        """
        category_id = self.request.query_params.get('category_id', None)
        if category_id is not None:
            queryset = queryset.filter(product_category_id=category_id)

        category_name = self.request.query_params.get('category_name', None)
        if category_name is not None:
            queryset = queryset.filter(product_category__name__contains=category_name)

        category_title = self.request.query_params.get('category_title', None)
        if category_title is not None:
            queryset = queryset.filter(product_category__title__contains=category_title)

        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__contains=name)

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
            queryset = queryset.filter(description__contains=description)

        return queryset

    def get_serializer_class(self):
        return ProductSerializer


class PriceViewset(ModelViewSet):
    # queryset = Price.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Price.objects.all()

        """
            Product Filter Options
        """
        product_id = self.request.query_params.get('product_id', None)
        if product_id is not None:
            queryset = queryset.filter(price_product_id=product_id)

        product_name = self.request.query_params.get('product_name', None)
        if product_name is not None:
            queryset = queryset.filter(price_product__name__contains=product_name)

        product_country = self.request.query_params.get('product_country', None)
        if product_country is not None:
            queryset = queryset.filter(price_product__country=product_country)

        product_province = self.request.query_params.get('product_province', None)
        if product_province is not None:
            queryset = queryset.filter(price_product__province=product_province)

        product_city = self.request.query_params.get('product_city', None)
        if product_city is not None:
            queryset = queryset.filter(price_product__city=product_city)

        product_city = self.request.query_params.get('product_city', None)
        if product_city is not None:
            queryset = queryset.filter(price_product__city=product_city)

        """
            Product Owner Filter Options
        """
        product_owner_id = self.request.query_params.get('product_owner_id', None)
        if product_owner_id is not None:
            queryset = queryset.filter(price_product__product_owner_id=product_owner_id)

        product_owner_name = self.request.query_params.get('product_owner_name', None)
        if product_owner_name is not None:
            queryset = queryset.filter(price_product__product_owner__name__contains=product_owner_name)

        product_owner_username = self.request.query_params.get('product_owner_username', None)
        if product_owner_username is not None:
            queryset = queryset.filter(price_product__product_owner__identity_user__username__contains=product_owner_username)

        product_owner_organization = self.request.query_params.get('product_owner_organization', None)
        if product_owner_organization is not None:
            queryset = queryset.filter(price_product__product_owner__identity_organization__name__contains=product_owner_organization)

        value = self.request.query_params.get('value', None)
        if value is not None:
            queryset = queryset.filter(value=value)

        return queryset

    def get_serializer_class(self):
        return PriceSerializer


class PictureViewset(ModelViewSet):
    # queryset = Picture.objects.all()
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
    # queryset = Comment.objects.all()
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
            queryset = queryset.filter(text__contains=text)

        return queryset

    def get_serializer_class(self):
        return CommentSerializer
