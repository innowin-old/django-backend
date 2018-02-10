from graphene import relay, AbstractType
from graphene_django.filter import DjangoFilterConnectionField

from products.schemas.queries.category import CategoryFilter, CategoryNode
from products.schemas.queries.product import ProductFilter, ProductNode


class ProductQuery(AbstractType):
    product_category = relay.Node.Field(CategoryNode)
    product_categories = DjangoFilterConnectionField(
        CategoryNode, filterset_class=CategoryFilter)
    product = relay.Node.Field(ProductNode)
    products = DjangoFilterConnectionField(ProductNode, filterset_class=ProductFilter)
