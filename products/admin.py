from django.contrib import admin
from django.utils.html import format_html

from products.models import Category, CategoryField, Product, Price, Picture, Comment


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['category_parent', 'name', 'title', 'creatable']


class CategoryFieldAdmin(admin.ModelAdmin):
    model = CategoryField
    list_display = ['field_category', 'name', 'title', 'type']


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['product_owner', 'category', 'name', 'country']


class PriceAdmin(admin.ModelAdmin):
    model = Price
    list_display = ['price_product', 'price']


class PictureAdmin(admin.ModelAdmin):
    model = Picture
    list_display = ['picture_product', 'order', 'picture_link']

    def picture_link(self, obj):
        return format_html(
            "<a href='%s'>%s</a>" %
            (obj.picture.file.url, obj.picture.file.url))


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ['comment_product', 'comment_user']


admin.site.register(Category, CategoryAdmin)
admin.site.register(CategoryField, CategoryFieldAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(Comment, CommentAdmin)
