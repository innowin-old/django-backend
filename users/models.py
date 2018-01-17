from __future__ import unicode_literals

import re

from django.db import models, transaction
from django.db.models.signals import post_save
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver

from danesh_boom.models import PhoneField
from media.models import Media
from organizations.models import Organization
from base.models import Base, BaseManager
from base.signals import update_cache


class Identity(Base):
    identity_user = models.OneToOneField(
        User,
        related_name="identity",
        on_delete=models.CASCADE,
        db_index=True,
        null=True,
        blank=True,
        help_text='Integer')
    identity_organization = models.OneToOneField(
        Organization,
        related_name="identity",
        on_delete=models.CASCADE,
        db_index=True,
        null=True,
        blank=True,
        help_text='Integer')
    name = models.CharField(max_length=150, db_index=True, unique=True, help_text='String(150)')

    objects = BaseManager()

    def clean(self):
        if not self.identity_user and not self.identity_organization:
            raise ValidationError(_('User or Organization should be set'))
        if self.identity_user and self.identity_organization:
            raise ValidationError(
                _('Only on of User or Organization should be set'))

    def __str__(self):
        return self.name

    def validate_user(self, user):
        if self.identity_user and self.identity_user == user:
            return True
        elif self.identity_organization and self.identity_organization.owner == user:
            return True
        return False

    def validate_organization(self, organization):
        if self.identity_organization == organization:
            return True
        return False

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Identity, self).save(*args, **kwargs)


default_user_save = User.save
# Cache Model Data After Update
post_save.connect(update_cache, sender=Identity)


def user_save(self, *args, **kwargs):
    with transaction.atomic():
        default_user_save(self, *args, **kwargs)
        if hasattr(self, 'identity'):
            identity = self.identity
        else:
            identity = Identity(identity_user=self)
        identity.name = self.username
        identity.save()


User.save = user_save


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile()
        profile.profile_user = instance
        profile.save()


class Profile(Base):
    profile_user = models.OneToOneField(User, related_name="profile",
                                on_delete=models.CASCADE, help_text='Integer')
    public_email = models.EmailField(null=True, blank=True, help_text='Email')
    national_code = models.CharField(max_length=20, blank=True,
                                     validators=[RegexValidator('^\d{10}$')], help_text='String(20)')
    birth_date = models.CharField(max_length=10, blank=True, null=True, help_text='String(10)')
    web_site = ArrayField(models.URLField(), blank=True, default=[], help_text='Array')
    phone = ArrayField(PhoneField(), blank=True, default=[], help_text='Array')
    mobile = ArrayField(PhoneField(), blank=True, default=[], help_text='Array')
    fax = PhoneField(blank=True, help_text='Phone')
    telegram_account = models.CharField(
        max_length=256, blank=True, validators=[
            RegexValidator('^@[\w\d_]+$')], help_text='String(256)')
    description = models.TextField(blank=True, help_text='Text')
    profile_media = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text='Integer')

    objects = BaseManager()

    def __str__(self):
        return self.profile_user.username

    def clean(self):
        if self.birth_date:
            p = re.compile('^\d{4}-\d{2}-\d{2}$')
            birth_date = self.birth_date
            if not re.match(p, birth_date):
                raise ValidationError(_('Invalid birth date'))
            now = timezone.now().date().strftime('%Y-%m-%d')
            if birth_date > now:
                raise ValidationError(_('Invalid birth date'))


# Cache Model Data After Update
post_save.connect(update_cache, sender=Profile)


class Education(Base):
    education_user = models.ForeignKey(User, related_name="educations",
                             on_delete=models.CASCADE, help_text='Integer')
    grade = models.CharField(max_length=100, help_text='String(100)')
    university = models.CharField(max_length=100, help_text='String(100)')
    field_of_study = models.CharField(max_length=100, help_text='String(100)')
    from_date = models.CharField(max_length=7, blank=True, null=True, help_text='String(7)')
    to_date = models.CharField(max_length=7, blank=True, null=True, help_text='String(7)')
    average = models.FloatField(
        validators=[
            MaxValueValidator(20),
            MinValueValidator(0)],
        null=True,
        blank=True,
        help_text='Float')
    description = models.TextField(blank=True, help_text='Text')

    objects = BaseManager()

    def __str__(self):
        return "%s(%s - %s)" % (
            self.education_user.username,
            self.grade,
            self.field_of_study
        )

    def clean(self):
        p = re.compile('^\d{4}-\d{2}$')
        from_date = to_date = None
        if self.from_date:
            from_date = self.from_date
            if not re.match(p, from_date):
                raise ValidationError(_('Invalid from date'))

        if self.to_date:
            to_date = self.to_date
            if not re.match(p, to_date):
                raise ValidationError(_('Invalid to date'))

        if from_date and to_date and from_date > to_date:
            raise ValidationError(_('To date must be greater than from date'))


# Cache Model Data After Update
post_save.connect(update_cache, sender=Education)


class Research(Base):
    research_user = models.ForeignKey(User, related_name="researches",
                             on_delete=models.CASCADE, help_text='Integer')
    title = models.CharField(max_length=250, help_text='String(250)')
    url = models.URLField(blank=True, help_text='URL')
    author = ArrayField(models.CharField(max_length=100), blank=True, help_text='Array(String(100))')
    publication = models.CharField(max_length=100, blank=True, help_text='String(100)')
    year = models.IntegerField(null=True, blank=True, help_text='Integer')
    page_count = models.IntegerField(null=True, blank=True, help_text='Integer')

    objects = BaseManager()

    def __str__(self):
        return "%s(%s)" % (self.research_user.username, self.title)


# Cache Model Data After Update
post_save.connect(update_cache, sender=Research)


class Certificate(Base):
    certificate_user = models.ForeignKey(User, related_name="certificates",
                             on_delete=models.CASCADE, help_text='Integer')
    title = models.CharField(max_length=250, help_text='String(250)')
    picture_media = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text='Integer')

    objects = BaseManager()

    def __str__(self):
        return "%s(%s)" % (self.certificate_user.username, self.title)


# Cache Model Data After Update
post_save.connect(update_cache, sender=Certificate)


class WorkExperience(Base):
    STATUSES = (
        ('WITHOUT_CONFIRM', 'بدون تایید'),
        ('WAIT_FOR_CONFIRM', 'منتظر تایید'),
        ('CONFIRMED', 'تایید شده'),
        ('UNCONFIRMED', 'تایید نشده'),
    )

    work_experience_user = models.ForeignKey(User, related_name="work_experiences",
                             on_delete=models.CASCADE, help_text='Integer')
    name = models.CharField(max_length=100, blank=True, help_text='String(100)')
    work_experience_organization = models.ForeignKey(
        Organization,
        related_name="work_experience_organization",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text='Integer')
    position = models.CharField(max_length=100, blank=True, help_text='String(100)')
    from_date = models.CharField(max_length=7, blank=True, null=True, help_text='String(100)')
    to_date = models.CharField(max_length=7, blank=True, null=True, help_text='String(7)')
    status = models.CharField(
        choices=STATUSES,
        max_length=20,
        default='WITHOUT_CONFIRM',
        help_text='WITHOUT_CONFIRM | WAIT_FOR_CONFIRM | CONFIRMED | UNCONFIRMED')

    objects = BaseManager()

    def __str__(self):
        return "%s(%s)" % (self.work_experience_user.username, self.name)

    def clean(self):
        if not self.work_experience_organization and not self.name:
            raise ValidationError(_('Please enter name or organization'))

        if self.work_experience_organization and self.name:
            raise ValidationError(_('Please enter name or organization'))

        if self.name and self.status != 'WITHOUT_CONFIRM':
            raise ValidationError(_('Invalid status'))

        p = re.compile('^\d{4}-\d{2}$')
        from_date = to_date = None
        if self.from_date:
            from_date = self.from_date
            if not re.match(p, from_date):
                raise ValidationError(_('Invalid from date'))

        if self.to_date:
            to_date = self.to_date
            if not re.match(p, to_date):
                raise ValidationError(_('Invalid to date'))

        if from_date and to_date and from_date > to_date:
            raise ValidationError(_('To date must be greater than from date'))


# Cache Model Data After Update
post_save.connect(update_cache, sender=WorkExperience)


class Skill(Base):
    skill_user = models.ForeignKey(User, related_name="skills",
                             on_delete=models.CASCADE, help_text='Integer')
    title = models.CharField(max_length=250, help_text='String(250)')
    tag = ArrayField(models.CharField(max_length=50), blank=True, help_text='50')
    description = models.TextField(blank=True, help_text='Text')

    objects = BaseManager()

    def __str__(self):
        return "%s(%s)" % (self.skill_user.username, self.title)


# Cache Model Data After Update
post_save.connect(update_cache, sender=Skill)


class Badge(Base):
    badge_user = models.ForeignKey(User, related_name="badges",
                             on_delete=models.CASCADE, help_text='Integer')
    title = models.CharField(max_length=100, help_text='String(100)')

    objects = BaseManager()

    def __str__(self):
        return "%s(%s)" % (self.badge_user.username, self.badge_user)


    class Meta:
        unique_together = (('badge_user', 'title'),)


# Cache Model Data After Update
post_save.connect(update_cache, sender=Badge)