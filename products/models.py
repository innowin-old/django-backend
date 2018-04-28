from django.db import models
from django.db.models.signals import post_save, pre_save
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User

from base.models import Base, BaseManager
from base.signals import update_cache, set_child_name
from media.models import Media
from users.models import Identity


class Category(Base):
    category_parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, db_index=True,
                                        help_text='Integer')
    name = models.CharField(max_length=100, unique=True, db_index=True, help_text='String(100)')
    title = models.CharField(max_length=100, db_index=True, help_text='String(100)')
    creatable = models.BooleanField(default=False, help_text='Boolean')

    objects = BaseManager()

    def __str__(self):
        return self.name


# Cache Model Data After Update
post_save.connect(update_cache, sender=Category)
# Set Child Name
pre_save.connect(set_child_name, sender=Category)


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

    field_category = models.ForeignKey(Category, related_name="category_fields", on_delete=models.CASCADE,
                                       db_index=True, help_text='Integer')
    name = models.CharField(max_length=100, unique=True, db_index=True, help_text='String(100)')
    title = models.CharField(max_length=100, db_index=True, help_text='String(100)')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default=STRING, db_index=True,
                            help_text='string | float | choices | bool')
    order = models.IntegerField(default=0, db_index=True, help_text='Integer')
    option = JSONField(null=True, blank=True, db_index=True, help_text='JSON')

    objects = BaseManager()

    def __str__(self):
        return self.name


# Cache Model Data After Update
post_save.connect(update_cache, sender=CategoryField)
# Set Child Name
pre_save.connect(set_child_name, sender=CategoryField)


class Product(Base):
    product_owner = models.ForeignKey(Identity, related_name="identity_products", on_delete=models.CASCADE,
                                      db_index=True, help_text='Integer')
    product_category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE, db_index=True,
                                         help_text='Integer')
    name = models.CharField(max_length=100, db_index=True, help_text='String(100)')
    country = models.CharField(max_length=50, db_index=True, help_text='String(50)')
    province = models.CharField(max_length=50, db_index=True, help_text='String(50)')
    city = models.CharField(max_length=50, blank=True, db_index=True, help_text='String(50)')
    description = models.CharField(max_length=1000, blank=True, db_index=True, help_text='String(1000)')
    attrs = JSONField(null=True, blank=True, help_text='JSON')
    custom_attrs = JSONField(null=True, blank=True, help_text='JSON')
    product_user = models.ForeignKey(User, related_name="user_products", on_delete=models.CASCADE, db_index=True, help_text="Integer")

    objects = BaseManager()

    def __str__(self):
        return self.name


# Cache Model Data After Update
post_save.connect(update_cache, sender=Product)
# Set Child Name
pre_save.connect(set_child_name, sender=Product)


class Price(Base):
    price_product = models.ForeignKey(Product, related_name="prices", on_delete=models.CASCADE, db_index=True,
                                      help_text='Integer')
    value = models.FloatField(help_text='Float')

    objects = BaseManager()

    def __str__(self):
        return '%s(%s)' % (self.price_product.name, self.price_product)


# Cache Model Data After Update
post_save.connect(update_cache, sender=Price)
# Set Child Name
pre_save.connect(set_child_name, sender=Price)


class Picture(Base):
    picture_product = models.ForeignKey(Product, related_name="product_pictures", on_delete=models.CASCADE,
                                        db_index=True, help_text='Integer')
    picture_media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name="product_picture_media",
                                      help_text='Integer')
    order = models.IntegerField(default=0, help_text='Integer')
    description = models.TextField(blank=True, db_index=True, help_text='Text')

    objects = BaseManager()

    def __str__(self):
        return self.picture_product.name


# Cache Model Data After Update
post_save.connect(update_cache, sender=Picture)
# Set Child Name
pre_save.connect(set_child_name, sender=Picture)


class Comment(Base):
    comment_product = models.ForeignKey(Product, related_name="product_comments", on_delete=models.CASCADE,
                                        db_index=True, help_text='Integer')
    comment_user = models.ForeignKey(User, related_name="user_product_comments", on_delete=models.CASCADE,
                                     db_index=True, help_text='Integer')
    text = models.TextField(db_index=True, help_text='Text')

    objects = BaseManager()

    def __str__(self):
        return '%s(%s)' % (self.comment_product.name, self.comment_user.username)


# Cache Model Data After Update
post_save.connect(update_cache, sender=Comment)
# Set Child Name
pre_save.connect(set_child_name, sender=Comment)
