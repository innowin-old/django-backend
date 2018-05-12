from rest_framework import status
from django.http.response import JsonResponse

from base.serializers import BaseSerializer
from users.serializers import UserMiniSerializer, IdentityMiniSerializer
from .models import (
        Category,
        CategoryField,
        Product,
        Price,
        Picture,
        Comment
    )


class CategorySerializer(BaseSerializer):
    class Meta:
        model = Category
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class CategoryFieldSerializer(BaseSerializer):
    class Meta:
        model = CategoryField
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class ProductSerializer(BaseSerializer):
    class Meta:
        model = Product
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
            'product_user': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get("request")
        if not request.user.is_superuser or 'product_user' not in validated_data:
            validated_data['product_user'] = request.user
        product = Product.objects.create(**validated_data)
        product.save()
        return product


class ProductListViewSerializer(BaseSerializer):
    product_category = CategorySerializer()
    product_user = UserMiniSerializer()
    product_owner = IdentityMiniSerializer()

    class Meta:
        model = Product
        exclude = ['child_name']


class PriceSerializer(BaseSerializer):
    class Meta:
        model = Price
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        '''
            post object level permission
        '''
        product_id = validated_data.get('price_product')
        product = Product.objects.get(pk=product_id)
        '''if product.product_user != request.user and not request.user.is_superuser:
            return JsonResponse(data={})'''
        '''
            create price object
        '''
        price = Price.objects.create(**validated_data)
        price.save()
        return price


class PictureSerializer(BaseSerializer):
    class Meta:
        model = Picture
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class CommentSerializer(BaseSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }
