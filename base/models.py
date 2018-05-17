from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.contrib.auth.models import User

from unixtimestampfield.fields import UnixTimeStampField

from .signals import update_cache, set_child_name


class BaseManager(models.Manager):
    def get_queryset(self):
        if not cache.get(self.model._meta.db_table):
            cache.set(self.model._meta.db_table, super(BaseManager, self).get_queryset().filter(delete_flag=False),
                      settings.CACHE_TIMEOUT)
        return cache.get(self.model._meta.db_table)


class Base(models.Model):
    class Meta:
        ordering = ["-pk"]
        verbose_name_plural = "Basics"

    created_time = models.DateTimeField(db_index=True, default=now, editable=False, blank=True)
    updated_time = models.DateTimeField(db_index=True, default=now, blank=True)
    delete_flag = models.BooleanField(db_index=True, default=False)
    child_name = models.CharField(max_length=50, blank=True)

    objects = BaseManager()


# Cache Model Data After Update
post_save.connect(update_cache, sender=Base)


class HashtagParent(Base):
    title = models.CharField(db_index=True, max_length=50, help_text='String(50)')

    objects = BaseManager()


# Cache Model Data After Update
post_save.connect(update_cache, sender=HashtagParent)
# Set Child Name
pre_save.connect(set_child_name, sender=HashtagParent)


class Hashtag(Base):
    title = models.CharField(db_index=True, max_length=50, help_text='String(50)')
    related_parent = models.ForeignKey(HashtagParent, related_name='nested_mentions', blank=True, null=True,
                                       db_index=True, on_delete=models.CASCADE, help_text='String(50)')
    hashtag_base = models.ForeignKey(Base, related_name='base_hashtags', on_delete=models.CASCADE, blank=True,
                                     null=True, db_index=True, help_text='Integer')

    objects = BaseManager()


# Cache Model Data After Update
post_save.connect(update_cache, sender=Hashtag)
# Set Child Name
pre_save.connect(set_child_name, sender=Hashtag)


class HashtagRelation(Base):
    hashtag_first = models.ForeignKey(HashtagParent, related_name='hashtag_first_relation', db_index=True,
                                      on_delete=models.CASCADE, help_text='Integer')
    hashtag_second = models.ForeignKey(HashtagParent, related_name='hashtag_second_relation', db_index=True,
                                       on_delete=models.CASCADE, help_text='Integer')
    active = models.BooleanField(default=True)

    objects = BaseManager()


# Cache Model Data After Update
post_save.connect(update_cache, sender=HashtagRelation)
# Set Child Name
pre_save.connect(set_child_name, sender=HashtagRelation)


class BaseComment(Base):
    comment_parent = models.ForeignKey(Base, related_name='base_comments', db_index=True, on_delete=models.CASCADE,
                                       help_text='Integer')
    comment_sender = models.ForeignKey('users.Identity', related_name='base_comment_senders', db_index=True,
                                       on_delete=models.CASCADE, help_text='Integer')
    comment_picture = models.ForeignKey('media.Media', on_delete=models.CASCADE, related_name="base_comment_picture",
                                        blank=True, null=True, help_text='Integer')
    text = models.TextField(help_text='Text')

    objects = BaseManager()


# Cache Model Data After Update
post_save.connect(update_cache, sender=BaseComment)
# Set Child Name
pre_save.connect(set_child_name, sender=BaseComment)


class Post(Base):
    POST_TYPES = (
        ('supply', 'عرضه'),
        ('demand', 'تقاضا'),
        ('post', 'پست'),
    )
    post_type = models.CharField(choices=POST_TYPES, default='post', max_length=10, help_text='supply | demand | post')
    post_user = models.ForeignKey(User, related_name="user_posts", on_delete=models.CASCADE, help_text='Integer', db_index=True)
    post_identity = models.ForeignKey('users.Identity', related_name="identity_posts", on_delete=models.CASCADE, help_text='Integer', db_index=True)
    post_related_product = models.ForeignKey('products.Product', related_name='product_related_posts', on_delete=models.CASCADE, help_text='Integer', db_index=True, blank=True, null=True)
    post_title = models.CharField(max_length=100, db_index=True, help_text='String(100)')
    post_description = models.TextField(max_length=300, db_index=True, help_text='String(300)', blank=True, null=True)
    post_picture = models.ForeignKey('media.Media', on_delete=models.CASCADE, help_text='Integer', blank=True,
                                     null=True, default=None)
    post_parent = models.ForeignKey(Base, related_name='base_posts', db_index=True, on_delete=models.CASCADE,
                                    blank=True, null=True, help_text='integer')
    post_pinned = models.BooleanField(default=False, help_text='Boolean')
    post_promote = UnixTimeStampField(auto_now_add=True, use_numeric=True, help_text='Unix Time Stamp', db_index=True)

    objects = BaseManager()

    def __str__(self):
        return self.post_identity.name

    @property
    def user_username(self):
        return self.post_identity.name


# Cache Model Data After Update
post_save.connect(update_cache, sender=Post)
# Set Child Name
pre_save.connect(set_child_name, sender=Post)


class BaseCertificate(Base):
    certificate_parent = models.ForeignKey(Base, related_name='base_certificates', db_index=True,
                                           on_delete=models.CASCADE,
                                           help_text='Integer')
    certificate_identity = models.ForeignKey('users.Identity', related_name='base_certificate_senders', db_index=True,
                                             on_delete=models.CASCADE, help_text='Integer')
    certificate_picture = models.ForeignKey('media.Media', on_delete=models.CASCADE,
                                            related_name="base_certificate_picture",
                                            help_text='Integer')
    title = models.CharField(max_length=250, help_text='String(250)')

    objects = BaseManager()

    def __str__(self):
        return "%s(%s)" % (self.certificate_identity.name, self.title)


# Cache Model Data After Update
post_save.connect(update_cache, sender=BaseCertificate)
# Set Child Name
pre_save.connect(set_child_name, sender=BaseCertificate)


class BaseRoll(Base):
    name = models.CharField(max_length=100)
    roll_owner = models.ForeignKey(Base, related_name='base_rolls', db_index=True,
                                   on_delete=models.CASCADE, help_text='Integer')
    user_roll = models.ManyToManyField(User, related_name='user_rolls', help_text='Integer')

    class Meta:
        unique_together = ('name', 'roll_owner',)


# Cache Model Data After Update
post_save.connect(update_cache, sender=BaseRoll)
# Set Child Name
pre_save.connect(set_child_name, sender=BaseRoll)


class RollPermission(Base):
    permission = models.CharField(max_length=50, choices=settings.ORGANIZATION_RELATED_MODELS_ACTIONS)
    roll_permission_related_roll = models.ForeignKey(BaseRoll, related_name='permission_rolls', db_index=True,
                                                     on_delete=models.CASCADE, help_text='Integer')

    class Meta:
        unique_together = ('permission', 'roll_permission_related_roll',)


# Cache Model Data After Update
post_save.connect(update_cache, sender=RollPermission)
# Set Child Name
pre_save.connect(set_child_name, sender=RollPermission)


class BaseCountry(Base):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, blank=True, null=True)


# Cache Model Data After Update
post_save.connect(update_cache, sender=BaseCountry)
# Set Child Name
pre_save.connect(set_child_name, sender=BaseCountry)


class BaseProvince(Base):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, blank=True, null=True)
    province_related_country = models.ForeignKey(BaseCountry, related_name='province_country', db_index=True,
                                                 on_delete=models.CASCADE, help_text='Integer')


# Cache Model Data After Update
post_save.connect(update_cache, sender=BaseProvince)
# Set Child Name
pre_save.connect(set_child_name, sender=BaseProvince)


class BaseTown(Base):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, blank=True, null=True)
    town_related_province = models.ForeignKey(BaseProvince, related_name='town_province', db_index=True,
                                              on_delete=models.CASCADE, help_text='Integer')


# Cache Model Data After Update
post_save.connect(update_cache, sender=BaseTown)
# Set Child Name
pre_save.connect(set_child_name, sender=BaseTown)


class BaseSocialType(Base):
    social_logo = models.CharField(max_length=255)
    social_name = models.CharField(max_length=30)
    social_base_url = models.CharField(max_length=50)
    social_sort = models.IntegerField()


# Cache Model Data After Update
post_save.connect(update_cache, sender=BaseSocialType)
# Set Child Name
pre_save.connect(set_child_name, sender=BaseSocialType)


class BaseSocial(Base):
    base_social_related_social_type = models.ForeignKey(BaseSocialType, related_name='base_social_parent',
                                                   db_index=True, on_delete=models.CASCADE, help_text='Integer')
    base_social_parent = models.ForeignKey(Base, related_name='social_parent', db_index=True, on_delete=models.CASCADE,
                                      help_text='Integer')


# Cache Model Data After Update
post_save.connect(update_cache, sender=BaseSocial)
# Set Child Name
pre_save.connect(set_child_name, sender=BaseSocial)