from django_filters import OrderingFilter, FilterSet
from graphene_django import DjangoObjectType
from graphene import relay, resolve_only_args
from graphene_django.filter import DjangoFilterConnectionField

from products.models import Product, Price, Picture, Comment
from products.schemas.queries.price import PriceFilter, PriceNode
from products.schemas.queries.picture import ProductPictureFilter, ProductPictureNode
from products.schemas.queries.comment import CommentFilter, CommentNode


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'country': ['exact', 'icontains', 'istartswith'],
            'province': ['exact', 'icontains', 'istartswith'],
            'city': ['exact', 'gte', 'lte'],
            # ---------- Category ------------
            'product_category__name': ['exact', 'icontains', 'istartswith'],
            'product_category__title': ['exact', 'icontains', 'istartswith'],
        }

    order_by = OrderingFilter(fields=('id', 'name', 'owner__name', 'product_category__name', 'province'))


class ProductNode(DjangoObjectType):
    product_prices = DjangoFilterConnectionField(
        PriceNode, filterset_class=PriceFilter)
    product_pictures = DjangoFilterConnectionField(
        ProductPictureNode, filterset_class=ProductPictureFilter)
    product_comments = DjangoFilterConnectionField(
        CommentNode, filterset_class=CommentFilter)

    @resolve_only_args
    def resolve_product_prices(self, **args):
        prices = Price.objects.filter(product=self)
        return PriceFilter(args, queryset=prices).qs

    @resolve_only_args
    def resolve_product_pictures(self, **args):
        pictures = Picture.objects.filter(product=self)
        return ProductPictureFilter(args, queryset=pictures).qs

    @resolve_only_args
    def resolve_product_comments(self, **args):
        comments = Comment.objects.filter(product=self)
        return CommentFilter(args, queryset=comments).qs

    class Meta:
        model = Product
        interfaces = (relay.Node,)
