from django.db import models
from django.contrib.postgres.fields import JSONField

from django.contrib.auth.models import User
from media.models import Media
from users.models import Identity
from base.models import Base


class Category(Base):
    category_parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, db_index=True)
    name = models.CharField(max_length=100, unique=True, db_index=True)
    title = models.CharField(max_length=100, db_index=True)
    creatable = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class CategoryField(Base):
    STRING = 'string'
    FLOAT = 'float'
    CHOICES = 'choices'
    BOOL = 'bool'
    TYPE_CHOICES = (
        (STRING, 'ارزش آن بصورت استرینگ پر شود'),
        (FLOAT, 'ارزش آن بصورت عدد پر شود'),
        (CHOICES, 'ارائه ارزش بصورت انتخابی'),
        (BOOL, 'ارئه ارزش بصورت چک باکس')
    )

    field_category = models.ForeignKey(Category, related_name="category_fields", on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=100, unique=True, db_index=True)
    title = models.CharField(max_length=100, db_index=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default=STRING, db_index=True)
    order = models.IntegerField(default=0, db_index=True)
    option = JSONField(null=True, blank=True, db_index=True)

    def __str__(self):
        return self.name


class Product(Base):
    product_owner = models.ForeignKey(Identity, related_name="identity_products", on_delete=models.CASCADE, db_index=True)
    product_category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=100, db_index=True)
    country = models.CharField(max_length=50, db_index=True)
    province = models.CharField(max_length=50, db_index=True)
    city = models.CharField(max_length=50, blank=True, db_index=True)
    description = models.CharField(max_length=1000, blank=True, db_index=True)
    attrs = JSONField(null=True, blank=True)
    custom_attrs = JSONField(null=True, blank=True)

    def __str__(self):
        return self.name


class Price(Base):
    price_product = models.ForeignKey(Product, related_name="prices", on_delete=models.CASCADE, db_index=True)
    value = models.FloatField()
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s(%s)' % (self.product.name, self.price)


class Picture(Base):
    picture_product = models.ForeignKey(Product, related_name="product_pictures", on_delete=models.CASCADE, db_index=True)
    picture_media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name="product_picture_media")
    order = models.IntegerField(default=0)
    description = models.TextField(blank=True, db_index=True)

    def __str__(self):
        return self.product.name


class Comment(Base):
    comment_product = models.ForeignKey(Product, related_name="product_comments", on_delete=models.CASCADE, db_index=True)
    comment_user = models.ForeignKey(User, related_name="user_product_comments", on_delete=models.CASCADE, db_index=True)
    text = models.TextField(db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s(%s)' % (self.product.name, self.user.username)
