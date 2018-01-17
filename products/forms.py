from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from products.models import Category, CategoryField, Product, Price, Picture, Comment


class CategoryForm(ModelForm):

    class Meta:
        model = Category
        exclude = ['parent']


class CategoryFieldForm(ModelForm):

    class Meta:
        model = CategoryField
        exclude = ['category']


class ProductForm(ModelForm):

    class Meta:
        model = Product
        exclude = ['owner', 'category']


class PriceForm(ModelForm):

    class Meta:
        model = Price
        exclude = ['product', 'create_time']

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise ValidationError(_('Price should be positive number'))
        return price


class PictureForm(ModelForm):

    class Meta:
        model = Picture
        exclude = ['product', 'picture']


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        exclude = ['product', 'user', 'create_time']
