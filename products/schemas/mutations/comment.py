from graphene import relay, Field, String, ID

from danesh_boom.viewer_fields import ViewerFields
from products.models import Product, Comment
from products.schemas.queries.comment import CommentNode
from products.forms import CommentForm
from utils.relay_helpers import get_node
from utils.Exceptions import ResponseError, FormError


class CreateCommentMutation(ViewerFields, relay.ClientIDMutation):
    """
    create product comment mutation
    possible error codes:
    - invalid_product
    - form_error
    """

    class Input:
        product_id = String(required=True)
        text = String(requeired=True)

    comment = Field(CommentNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user

        product_id = input.get('product_id')
        product = get_node(product_id, context, info, Product)
        if not product:
            raise ResponseError(
                "Invalid Product",
                code='invalid_product')

        # create comment
        form = CommentForm(input)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.product = product
            new_comment.user = user
            new_comment.save()
        else:
            raise FormError(form.errors)

        return CreateCommentMutation(comment=new_comment)


class UpdateCommentMutation(ViewerFields, relay.ClientIDMutation):
    """
    update product comment mutation
    possible error codes:
    - invalid_comment
    - form_error
    """

    class Input:
        id = String(required=True)
        text = String(requeired=True)

    comment = Field(CommentNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user

        comment_id = input.get('id')
        comment = get_node(comment_id, context, info, Comment)
        if not comment or comment.user != user:
            raise ResponseError(
                "Invalid Comment",
                code='invalid_comment')

        # update comment
        form = CommentForm(input, instance=comment)
        if form.is_valid():
            form.save()
        else:
            raise FormError(form.errors)

        return UpdateCommentMutation(comment=comment)


class DeleteCommentMutation(ViewerFields, relay.ClientIDMutation):
    """
    delete product comment mutation
    possible error codes:
    - invalid_comment
    """

    class Input:
        id = String(required=True)

    deleted_id = ID()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        user = context.user

        comment_id = input.get('id')
        comment = get_node(comment_id, context, info, Comment)
        if not comment or comment.user != user:
            raise ResponseError(
                "Invalid Comment",
                code='invalid_comment')

        # delete comment
        comment.delete()

        return DeleteCommentMutation(deleted_id=comment_id)
