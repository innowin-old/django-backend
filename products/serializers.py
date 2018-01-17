from rest_framework.serializers import ModelSerializer
from base.serializers import BaseSerializer
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
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class CategoryFieldSerializer(BaseSerializer):
    class Meta:
        model = CategoryField
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class ProductSerializer(BaseSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class PriceSerializer(BaseSerializer):
    class Meta:
        model = Price
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


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
