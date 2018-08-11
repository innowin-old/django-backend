import json

from django.http import Http404
from rest_framework import status

from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import list_route
from rest_framework.response import Response

from base.permissions import IsAdminUserOrReadOnly, IsOwnerOrReadOnly
from base.views import BaseModelViewSet
from .permissions import (
    IsPriceProductOwnerOrReadOnly,
    IsPictureProductOwnerOrReadOnly,
    IsCommentOwnerOrReadOnly,
    IsProductOrganizationOwnerOrReadOnly
)

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
    ProductListViewSerializer,
    ProductReadSerializer,
    PriceSerializer,
    PictureSerializer,
    CommentSerializer,
)


class CategoryViewset(BaseModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]

    def get_queryset(self):
        queryset = Category.objects.filter(delete_flag=False)

        parent_id = self.request.query_params.get('parent_id', None)
        if parent_id is not None:
            queryset = queryset.filter(category_parent_id=parent_id)

        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__contains=title)

        return queryset

    @list_route(methods=['post'], permission_classes=[IsAdminUser])
    def import_categories(self, request):
        jsonString = request.data.get('records')
        records = json.loads(jsonString)
        error_logs = []
        for record in records:
            try:
                category = Category.objects.create(name=record.get('name', None), title=record.get('name', None))
            except Exception as e:
                error_logs.append({
                    'data': record,
                    'status': str(e)
                })
                category = None
            if record.get('parent', None) is not None and record.get('parent', None) != '' and category is not None:
                try:
                    category_parent = Category.objects.get(name=record.get('parent', None))
                except Exception as e:
                    error_logs.append({
                        'data': record,
                        'status': str(e)
                    })
                    category_parent = None
                if category_parent is None:
                    try:
                        category_parent = Category.objects.create(name=record.get('parent', None),
                                                                  title=record.get('parent', None))
                    except Exception as e:
                        error_logs.append({
                            'data': record,
                            'status': str(e)
                        })
                category.category_parent = category_parent
                category.save()
        response = {'errors': error_logs}
        return Response(response, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        return CategorySerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryFieldViewset(BaseModelViewSet):
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = CategoryField.objects.filter(delete_flag=False)

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

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewset(BaseModelViewSet):
    owner_field = 'product_user'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsProductOrganizationOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Product.objects.filter(delete_flag=False)

        """
            Owner Filter Filters
        """
        product_user = self.request.query_params.get('product_user', None)
        if product_user is not None:
            queryset = queryset.filter(product_user=product_user)

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
            Product Category Filter
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
        if self.action == 'list':
            return ProductListViewSerializer
        elif self.action == 'retrieve':
            return ProductReadSerializer
        return ProductSerializer

    @list_route(
        permission_classes=[IsAdminUser],
        methods=['post']
    )
    def import_products(self, request):
        jsonString = request.data.get('records', None)
        data = json.loads(jsonString)
        errors = []
        for record in data:
            try:
                product = Product.objects.create(
                    name=record.get('name', None),
                    country=record.get('country', None),
                    province=record.get('province', None),
                    city=record.get('city', None),
                    description=record.get('description', None),
                    attrs=record.get('attrs', None),
                    custom_attrs=record.get('custom_attrs', None),
                    product_owner=record.get('product_owner', None),
                    product_user=record.get('product_user', None),
                    product_category=record.get('product_category', None)
                )
            except Exception as e:
                errors.append({
                    'data': record,
                    'status': str(e)
                })
        response = {
            'errors': errors
        }
        return Response(response)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class PriceViewset(BaseModelViewSet):
    permission_classes = [IsAuthenticated, IsPriceProductOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Price.objects.filter(delete_flag=False)

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
            queryset = queryset.filter(
                price_product__product_owner__identity_user__username__contains=product_owner_username)

        product_owner_organization = self.request.query_params.get('product_owner_organization', None)
        if product_owner_organization is not None:
            queryset = queryset.filter(
                price_product__product_owner__identity_organization__name__contains=product_owner_organization)

        value = self.request.query_params.get('value', None)
        if value is not None:
            queryset = queryset.filter(value=value)

        return queryset

    def get_serializer_class(self):
        return PriceSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class PictureViewset(BaseModelViewSet):
    permission_classes = [IsAuthenticated, IsPictureProductOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Picture.objects.all().filter(delete_flag=False).order_by('order')

        product = self.request.query_params.get('product', None)
        if product is not None:
            queryset = queryset.filter(picture_product_id=product)

        description = self.request.query_params.get('description', None)
        if description is not None:
            queryset = queryset.filter(description=description)

        return queryset

    def get_serializer_class(self):
        return PictureSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewset(BaseModelViewSet):
    permission_classes = [IsAuthenticated, IsCommentOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.filter(delete_flag=False)

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

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
