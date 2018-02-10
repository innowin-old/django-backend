from graphene import AbstractType

from products.schemas.mutations.category import CreateCategoryMutation,\
    UpdateCategoryMutation, DeleteCategoryMutation
from products.schemas.mutations.category_field import CreateCategoryFieldMutation,\
    UpdateCategoryFieldMutation, DeleteCategoryFieldMutation
from products.schemas.mutations.product import CreateProductMutation,\
    UpdateProductMutation, DeleteProductMutation
from products.schemas.mutations.price import CreatePriceMutation,\
    UpdatePriceMutation, DeletePriceMutation
from products.schemas.mutations.picture import CreateProductPictureMutation,\
    UpdateProductPictureMutation, DeleteProductPictureMutation
from products.schemas.mutations.comment import CreateCommentMutation,\
    UpdateCommentMutation, DeleteCommentMutation


class ProductMutation(AbstractType):
    # ---------------- Category ----------------
    create_product_category = CreateCategoryMutation.Field()
    update_product_category = UpdateCategoryMutation.Field()
    delete_product_category = DeleteCategoryMutation.Field()

    # ---------------- CategoryField ----------------
    create_product_category_field = CreateCategoryFieldMutation.Field()
    update_product_category_field = UpdateCategoryFieldMutation.Field()
    delete_product_category_field = DeleteCategoryFieldMutation.Field()

    # ---------------- Product ----------------
    create_product = CreateProductMutation.Field()
    update_product = UpdateProductMutation.Field()
    delete_product = DeleteProductMutation.Field()

    # ---------------- Price ----------------
    create_product_price = CreatePriceMutation.Field()
    update_product_price = UpdatePriceMutation.Field()
    delete_product_price = DeletePriceMutation.Field()

    # ---------------- Picture ----------------
    create_product_picture = CreateProductPictureMutation.Field()
    update_product_picture = UpdateProductPictureMutation.Field()
    delete_product_picture = DeleteProductPictureMutation.Field()

    # ---------------- Comment ----------------
    create_product_comment = CreateCommentMutation.Field()
    update_product_comment = UpdateCommentMutation.Field()
    delete_product_comment = DeleteCommentMutation.Field()
