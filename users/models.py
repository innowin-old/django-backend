from __future__ import unicode_literals

import re

from django.db import models, transaction
from django.db.models.signals import post_save, pre_save
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver

from danesh_boom.models import PhoneField
from django.contrib.postgres.fields import JSONField
from media.models import Media
from organizations.models import Organization
from base.models import Base, BaseManager, BaseCountry, BaseProvince, BaseTown
from base.signals import update_cache, set_child_name


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
    accepted = models.BooleanField(default=False)
    mobile_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    objects = BaseManager()

    def clean(self):
        if not self.identity_user and not self.identity_organization:
            raise ValidationError(_('User or Organization should be set'))
        if self.identity_user and self.identity_organization:
            raise ValidationError(
                _('Only on of User or Organization should be set'))

    def __str__(self):
        return self.name

    def validate_user(self, identity_user):
        if self.identity_user and self.identity_user == identity_user:
            return True
        elif self.identity_organization and self.identity_organization.owner == identity_user:
            return True
        return False

    def validate_organization(self, identity_organization):
        if self.identity_organization == identity_organization:
            return True
        return False

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Identity, self).save(*args, **kwargs)


default_user_save = User.save
# Cache Model Data After Update
post_save.connect(update_cache, sender=Identity)
# Set Child Name
pre_save.connect(set_child_name, sender=Identity)


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
        Profile.objects.create(profile_user=instance)


class Profile(Base):
    GENDER = (
        ('male', 'مرد'),
        ('female', 'زن')
    )
    profile_user = models.OneToOneField(User, related_name="profile",
                                        on_delete=models.CASCADE, help_text='Integer')
    public_email = models.EmailField(null=True, blank=True, help_text='Email')
    national_code = models.CharField(max_length=10, blank=True,
                                     validators=[RegexValidator('^\d{10}$')], help_text='String(20)')
    profile_media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name="users_profile_media",
                                      help_text='Integer', blank=True, null=True)
    birth_date = models.CharField(max_length=10, blank=True, null=True, help_text='String(10)')
    web_site = ArrayField(models.URLField(), blank=True, default=[], help_text='Array')
    phone = ArrayField(PhoneField(), blank=True, default=[], help_text='Array')
    mobile = ArrayField(PhoneField(), blank=True, default=[], help_text='Array')
    fax = PhoneField(blank=True, help_text='Phone')
    telegram_account = models.CharField(
        max_length=256, blank=True, validators=[
            RegexValidator('^@[\w\d_]+$')], help_text='String(256)')
    description = models.TextField(blank=True, help_text='Text', max_length=70)
    gender = models.CharField(
        choices=GENDER,
        max_length=7,
        default='Male',
        help_text='Male | Female'
    )
    is_plus_user = models.BooleanField(default=False)
    google_plus_address = models.CharField(max_length=255, blank=True, null=True)
    social_image_url = models.CharField(max_length=255, blank=True, null=True)
    linkedin_headline = models.CharField(max_length=255, blank=True, null=True)
    linkedin_positions = models.TextField(blank=True, null=True)
    yahoo_contacts = models.TextField(blank=True, null=True)
    profile_strength = models.SmallIntegerField(default=10)
    address = models.CharField(max_length=100, blank=True, null=True)
    profile_rellated_country = models.ForeignKey(BaseCountry, related_name='profile_country', db_index=True, blank=True
                                                 , null=True, on_delete=models.CASCADE, help_text='Integer')
    profile_rellated_province = models.ForeignKey(BaseProvince, related_name='profile_province', db_index=True, blank=True,
                                                  null=True, on_delete=models.CASCADE, help_text='Integer')
    profile_rellated_town = models.ForeignKey(BaseTown, related_name='profile_town', db_index=True, blank=True, null=True,
                                              on_delete=models.CASCADE, help_text='Integer')
    profile_banner = models.ForeignKey(Media, on_delete=models.CASCADE, related_name="users_banner_media",
                                       help_text='Integer', blank=True, null=True)

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
# Set Child Name
pre_save.connect(set_child_name, sender=Profile)


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
    description = models.TextField(blank=True, help_text='Text', max_length=30)

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
# Set Child Name
pre_save.connect(set_child_name, sender=Education)


class Research(Base):
    research_user = models.ForeignKey(User, related_name="researches",
                                      on_delete=models.CASCADE, help_text='Integer')
    title = models.CharField(max_length=250, help_text='String(250)')
    url = models.URLField(blank=True, help_text='URL')
    author = ArrayField(models.CharField(max_length=100), blank=True, help_text='Array(String(100))')
    publication = models.CharField(max_length=100, blank=True, help_text='String(100)')
    year = models.IntegerField(null=True, blank=True, help_text='Integer')
    page_count = models.IntegerField(null=True, blank=True, help_text='Integer')
    research_link = models.CharField(max_length=255, blank=True, null=True, help_text='String(255)')

    objects = BaseManager()

    def __str__(self):
        return "%s(%s)" % (self.research_user.username, self.title)


# Cache Model Data After Update
post_save.connect(update_cache, sender=Research)
# Set Child Name
pre_save.connect(set_child_name, sender=Research)


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
# Set Child Name
pre_save.connect(set_child_name, sender=Certificate)


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
        help_text='Integer')
    position = models.CharField(max_length=100, blank=True, help_text='String(100)')
    from_date = models.CharField(max_length=10, blank=True, null=True, help_text='String(10)')
    to_date = models.CharField(max_length=10, blank=True, null=True, help_text='String(10)')
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
# Set Child Name
pre_save.connect(set_child_name, sender=WorkExperience)


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
# Set Child Name
pre_save.connect(set_child_name, sender=Skill)


class Badge(Base):
    badge_user = models.ForeignKey(User, related_name="badges",
                                   on_delete=models.CASCADE, help_text='Integer')
    title = models.CharField(max_length=100, help_text='String(100)')

    objects = BaseManager()

    def __str__(self):
        return "%s(%s)" % (self.badge_user.username, self.badge_user)


# Cache Model Data After Update
post_save.connect(update_cache, sender=Badge)
# Set Child Name
pre_save.connect(set_child_name, sender=Badge)


class IdentityUrl(Base):
    url = models.CharField(max_length=50, db_index=True, help_text='String(50)', unique=True)
    identity_url_related_identity = models.OneToOneField(Identity, related_name='urls', on_delete=models.CASCADE, help_text='Integer')


# Cache Model Data After Update
post_save.connect(update_cache, sender=IdentityUrl)
# Set Child Name
pre_save.connect(set_child_name, sender=IdentityUrl)


class UserArticle(Base):
    user_article_related_user = models.ForeignKey(User, related_name="articles",
                                                  on_delete=models.CASCADE, help_text='Integer')
    doi_link = models.URLField(db_index=True)
    doi_meta = JSONField()
    publisher = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    article_author = ArrayField(models.CharField(max_length=255), blank=True, default=[], help_text='Array')


# Cache Model Data After Update
post_save.connect(update_cache, sender=UserArticle)
# Set Child Name
pre_save.connect(set_child_name, sender=UserArticle)


class Agent(Base):
    agent_identity = models.ForeignKey(Identity, related_name='agent', on_delete=models.CASCADE, help_text='Integer')


# Cache Model Data After Update
post_save.connect(update_cache, sender=Agent)
# Set Child Name
pre_save.connect(set_child_name, sender=Agent)


class Device(Base):
    device_user = models.ForeignKey(User, related_name='devices', on_delete=models.CASCADE, help_text='Integer')
    fingerprint = models.CharField(max_length=50)
    browser_name = models.CharField(max_length=20, blank=True, null=True)
    browser_version = models.CharField(max_length=30, blank=True, null=True)
    browser_major_version = models.SmallIntegerField(blank=True, null=True)
    browser_engine = models.CharField(max_length=20, blank=True, null=True)
    browser_engine_version = models.CharField(max_length=30, blank=True, null=True)
    browser_plugins = models.CharField(max_length=255, blank=True, null=True)
    browser_canvas_print = models.BooleanField(default=False)
    device_os = models.CharField(max_length=20, blank=True, null=True)
    device_os_version = models.CharField(max_length=30, blank=True, null=True)
    device_type = models.CharField(max_length=10, blank=True, null=True)
    device_vendor = models.CharField(max_length=20, blank=True, null=True)
    device_cpu = models.CharField(max_length=10, blank=True, null=True)
    device_current_screen_resolution = models.CharField(max_length=12, blank=True, null=True)
    device_available_screen_resolution = models.CharField(max_length=12, blank=True, null=True)
    device_agent = models.CharField(max_length=255, blank=True, null=True)
    device_color_depth = models.SmallIntegerField(blank=True, null=True)
    device_xdpi = models.SmallIntegerField(blank=True, null=True)
    device_ydpi = models.SmallIntegerField(blank=True, null=True)
    device_local_storage = models.BooleanField(default=False)


# Cache Model Data After Update
post_save.connect(update_cache, sender=Device)
# Set Child Name
pre_save.connect(set_child_name, sender=Device)


@receiver(post_save, sender=User)
def create_strength(sender, instance, created, **kwargs):
    if created:
        StrengthStates.objects.create(strength_user=instance)


class StrengthStates(Base):
    strength_user = models.OneToOneField(User, related_name='strength', db_index=True, on_delete=models.CASCADE, help_text='Integer')
    registration_obtained = models.BooleanField(default=False)
    profile_media_obtained = models.BooleanField(default=False)
    first_last_name_obtained = models.BooleanField(default=False)
    hashtags_obtained = models.BooleanField(default=False)
    exchange_obtained = models.BooleanField(default=False)
    follow_obtained = models.BooleanField(default=False)
    post_obtained = models.BooleanField(default=False)
    supply_demand_obtained = models.BooleanField(default=False)
    certificate_obtained = models.BooleanField(default=False)
    badge_obtained = models.BooleanField(default=False)
    mobile_verification_obtained = models.BooleanField(default=False)
    email_verification_obtained = models.BooleanField(default=False)
    education_obtained = models.BooleanField(default=False)
    brought_obtained = models.BooleanField(default=False)
    work_obtained = models.BooleanField(default=False)


# Cache Model Data After Update
post_save.connect(update_cache, sender=StrengthStates)
# Set Child Name
pre_save.connect(set_child_name, sender=StrengthStates)


class UserMetaData(Base):
    META_TYPES = (
        ('phone', 'شماره تلفن'),
        ('mobile', 'شماه همراه'),
        ('email', 'آدرس ایمیل'),
    )
    user_meta_type = models.CharField(choices=META_TYPES, max_length=20)
    user_meta_value = models.CharField(max_length=20, db_index=True)
    user_meta_related_user = models.ForeignKey(User, related_name='meta_data_user', blank=True, null=True,
                                               db_index=True, on_delete=models.CASCADE, help_text='Integer')


# Cache Model Data After Update
post_save.connect(update_cache, sender=UserMetaData)
# Set Child Name
pre_save.connect(set_child_name, sender=UserMetaData)