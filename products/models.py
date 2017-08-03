from django.db import models
from django.contrib.postgres.fields import JSONField

from django.contrib.auth.models import User
from media.models import Media
from users.models import Identity


class Category(models.Model):
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=100)
    creatable = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class CategoryField(models.Model):
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

    category = models.ForeignKey(Category, related_name="category_fields", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default=STRING)
    order = models.IntegerField(default=0)
    option = JSONField(null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    owner = models.ForeignKey(Identity, related_name="identity_products", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=1000, blank=True)
    attrs = JSONField(null=True, blank=True)
    custom_attrs = JSONField(null=True, blank=True)

    def __str__(self):
        return self.name


class Price(models.Model):
    product = models.ForeignKey(Product, related_name="prices", on_delete=models.CASCADE)
    price = models.FloatField()
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s(%s)' % (self.product.name, self.price)


class Picture(models.Model):
    product = models.ForeignKey(Product, related_name="pictures", on_delete=models.CASCADE)
    picture = models.ForeignKey(Media, on_delete=models.CASCADE, related_name="product_picture")
    order = models.IntegerField(default=0)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.product.name


class Comment(models.Model):
    product = models.ForeignKey(Product, related_name="product_comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="user_product_comments", on_delete=models.CASCADE)
    text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s(%s)' % (self.product.name, self.user.username)
