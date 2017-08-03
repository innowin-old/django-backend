from graphene import relay, Field, String, ID, Float

from danesh_boom.viewer_fields import ViewerFields
from products.models import Product, Price
from products.schemas.queries.price import PriceNode
from products.forms import PriceForm
from utils.relay_helpers import get_node
from utils.Exceptions import ResponseError, FormError


class CreatePriceMutation(ViewerFields, relay.ClientIDMutation):
    """
    create product price mutation
    possible error codes:
    - invalid_product
    - invalid_owner
    - form_error
    """

    class Input:
        product_id = String(required=True)
        price = Float(requeired=True)

    price = Field(PriceNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user

        product_id = input.get('product_id')
        product = get_node(product_id, context, info, Product)
        if not product:
            raise ResponseError(
                "Invalid Product",
                code='invalid_product')

        if not product.owner.validate_user(user):
            raise ResponseError(
                "Invalid Owner",
                code='invalid_owner')

        # create price
        form = PriceForm(input)
        if form.is_valid():
            new_price = form.save(commit=False)
            new_price.product = product
            new_price.save()
        else:
            raise FormError(form.errors)

        return CreatePriceMutation(price=new_price)


class UpdatePriceMutation(ViewerFields, relay.ClientIDMutation):
    """
    update product price mutation
    possible error codes:
    - invalid_price
    - invalid_owner
    - form_error
    """

    class Input:
        id = String(required=True)
        price = Float(requeired=True)

    price = Field(PriceNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user

        price_id = input.get('id')
        price = get_node(price_id, context, info, Price)
        if not price:
            raise ResponseError(
                "Invalid Price",
                code='invalid_price')

        if not price.product.owner.validate_user(user):
            raise ResponseError(
                "Invalid Owner",
                code='invalid_owner')

        # update price
        form = PriceForm(input, instance=price)
        if form.is_valid():
            form.save()
        else:
            raise FormError(form.errors)

        return UpdatePriceMutation(price=price)


class DeletePriceMutation(ViewerFields, relay.ClientIDMutation):
    """
    delete product price mutation
    possible error codes:
    - invalid_price
    - invalid_owner
    """

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user

        price_id = input.get('id', None)
        price = get_node(price_id, context, info, Price)
        if not price:
            raise ResponseError(
                "Invalid Price",
                code='invalid_price')

        if not price.product.owner.validate_user(user):
            raise ResponseError(
                "Invalid Owner",
                code='invalid_owner')

        # delete price
        price.delete()

        return DeletePriceMutation(deleted_id=price_id)
