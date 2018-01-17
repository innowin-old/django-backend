from graphene import relay, Field, String, Int, ID

from danesh_boom.viewer_fields import ViewerFields
from products.models import Product, Picture
from products.schemas.queries.picture import ProductPictureNode
from products.forms import PictureForm
from media.models import Media
from utils.relay_helpers import get_node
from utils.Exceptions import ResponseError, FormError


class CreateProductPictureMutation(ViewerFields, relay.ClientIDMutation):
    """
    create product picture mutation
    possible error codes:
    - invalid_product
    - invalid_owner
    - invalid_media
    - form_error
    """

    class Input:
        product_id = String(required=True)
        picture_id = String(required=True)
        order = Int(required=True)
        description = String()

    picture = Field(ProductPictureNode)

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

        media_id = input.get('picture_id')
        media = get_node(media_id, context, info, Media)

        if not media or not media.identity.validate_user(user):
            raise ResponseError(
                "Invalid Media",
                code='invalid_media')

        # create picture
        form = PictureForm(input, context.FILES)
        if form.is_valid():
            new_picture = form.save(commit=False)
            new_picture.product = product
            new_picture.picture = media
            new_picture.save()
        else:
            raise FormError(form.errors)

        return CreateProductPictureMutation(picture=new_picture)


class UpdateProductPictureMutation(ViewerFields, relay.ClientIDMutation):
    """
    update product picture mutation
    possible error codes:
    - invalid_picture
    - invalid_owner
    - invalid_media
    - form_error
    """

    class Input:
        id = String(required=True)
        picture_id = String(required=True)
        order = Int(requeired=True)
        description = String()

    picture = Field(ProductPictureNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user

        picture_id = input.get('id')
        picture = get_node(picture_id, context, info, Picture)
        if not picture:
            raise ResponseError(
                "Invalid Picture",
                code='invalid_picture')

        if not picture.product.owner.validate_user(user):
            raise ResponseError(
                "Invalid Owner",
                code='invalid_owner')

        media_id = input.get('picture_id')
        media = get_node(media_id, context, info, Media)

        if not media or not media.identity.validate_user(user):
            raise ResponseError(
                "Invalid Media",
                code='invalid_media')

        # update picture
        picture.picture = media

        form = PictureForm(input, instance=picture)
        if form.is_valid():
            form.save()
        else:
            raise FormError(form.errors)

        return UpdateProductPictureMutation(picture=picture)


class DeleteProductPictureMutation(ViewerFields, relay.ClientIDMutation):
    """
    delete product picture mutation
    possible error codes:
    - invalid_picture
    - invalid_owner
    """

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user

        picture_id = input.get('id')
        picture = get_node(picture_id, context, info, Picture)
        if not picture:
            raise ResponseError(
                "Invalid Picture",
                code='invalid_picture')

        if not picture.product.owner.validate_user(user):
            raise ResponseError(
                "Invalid Owner",
                code='invalid_owner')

        # delete product
        picture.delete()

        return DeleteProductPictureMutation(deleted_id=picture_id)
