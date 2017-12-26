from django.db import models
from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User

from unixtimestampfield.fields import UnixTimeStampField

from media.models import Media


class Base(models.Model):
    class Meta:
        ordering = ["-pk"]
        verbose_name_plural = "Basics"

    created_time = models.DateTimeField(db_index=True, default=now, editable=False, blank=True)
    updated_time = models.DateTimeField(db_index=True, default=now, blank=True)


class HashtagParent(Base):
    title = models.CharField(db_index=True, max_length=50, help_text='String(50)')


class Hashtag(Base):
    title = models.CharField(db_index=True, max_length=50, help_text='String(50)')
    related_parent = models.ForeignKey(HashtagParent, related_name='nested_mentions', blank=True, null=True, db_index=True, on_delete=models.CASCADE, help_text='String(50)')
    hashtag_base = models.ForeignKey(Base, related_name='base_hashtags', on_delete=models.CASCADE, blank=True, null=True, db_index=True, help_text='Integer')


class BaseComment(Base):
    comment_parent = models.ForeignKey(Base, related_name='base_comments', db_index=True, on_delete=models.CASCADE, help_text='Integer')
    comment_sender = models.ForeignKey('users.Identity', related_name='base_comment_senders', db_index=True, on_delete=models.CASCADE, help_text='Integer')
    comment_picture = models.ForeignKey('media.Media', on_delete=models.CASCADE, related_name="base_comment_picture", help_text='Integer')
    text = models.TextField(help_text='Text')


class Post(Base):
    POST_TYPES = (
        ('supply', 'عرضه'),
        ('demand', 'تقاضا'),
        ('post', 'پست'),
    )
    post_type = models.CharField(choices=POST_TYPES, default='post', max_length=10, help_text='supply | demand | post')
    post_user = models.ForeignKey(User, related_name="user_posts", on_delete=models.CASCADE, help_text='Integer', db_index=True)
    post_title = models.CharField(max_length=100, db_index=True, help_text='String(100)')
    post_description = models.TextField(max_length=300, db_index=True, help_text='String(300)', blank=True, null=True)
    post_picture = models.ForeignKey(Media, on_delete=models.CASCADE, help_text='Integer', blank=True, null=True)
    post_parent = models.ForeignKey(Base, related_name='base_posts', db_index=True, on_delete=models.CASCADE, help_text='integer')
    post_pinned = models.BooleanField(default=False, help_text='Boolean')
    post_promote = UnixTimeStampField(auto_now_add=True, use_numeric=True, help_text='Unix Time Stamp', db_index=True)

    def __str__(self):
        return self.post_user.username

    @property
    def user_username(self):
        return self.post_user.username