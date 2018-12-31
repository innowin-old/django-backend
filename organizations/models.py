from django.db import models, transaction
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator, MinValueValidator
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

from danesh_boom.models import PhoneField
from media.models import Media
from base.models import Base, BaseManager
from base.signals import update_cache, set_child_name


class Organization(Base):
    OWNERSHIP_TYPES = (
        ('idi', 'موسسه انفرادی'),
        ('org', 'شرکت'),
        ('cop', 'تعاونی'),
        ('pvt', 'سهامی خاص'),
        ('llp', 'سهامی عام'),
        ('gco', 'شرکت دولتی'),
        ('oth', 'سایر'),
    )

    BUSINESS_TYPES = (
        ('producer', 'تولید کننده'),
        ('investor', 'سرمایه گذار'),
        ('service provider', 'ارائه دهنده خدمات'),
    )

    owner = models.ForeignKey(User, related_name="organizations", db_index=True,
                              on_delete=models.CASCADE, help_text='Integer', blank=True, null=True)
    admins = models.ManyToManyField(User,
                                    related_name="organization_admins",
                                    blank=True,
                                    help_text='Integer')
    username = models.CharField(max_length=32, unique=True, help_text='String(32)', validators=[MinLengthValidator(3)], db_index=True)
    email = models.EmailField(blank=True, null=True, help_text='Text', db_index=True)
    public_email = models.EmailField(blank=True, null=True, help_text='Text', db_index=True)
    nike_name = models.CharField(max_length=20, db_index=True, null=True, blank=True, help_text='String(100)')
    official_name = models.CharField(max_length=50, db_index=True, unique=True, help_text='String(50)')
    national_code = models.CharField(max_length=11, db_index=True, null=True, blank=True, help_text='String(20)')
    registration_ads_url = models.URLField(db_index=True, null=True, blank=True, help_text='URL')
    registrar_organization = models.CharField(max_length=100, db_index=True, null=True, blank=True,
                                              help_text='String(100)')
    country = models.CharField(max_length=50, db_index=True, null=True, blank=True, help_text='String(50)')
    province = models.CharField(max_length=50, db_index=True, null=True, blank=True, help_text='String(50)')
    city = models.CharField(max_length=50, db_index=True, null=True, blank=True, help_text='String(50)')
    address = models.TextField(blank=True, null=True, db_index=True, help_text='Text')
    phone = models.CharField(max_length=11, blank=True, null=True, help_text='Phone', validators=[RegexValidator('^[0][0-9]{10,10}$')], db_index=True)
    web_site = models.TextField(max_length=100, null=True, db_index=True, blank=True, help_text='URL')
    established_year = models.PositiveIntegerField(null=True, db_index=True, blank=True, help_text='Integer', validators=[MinValueValidator(1300)])
    ownership_type = models.CharField(
        choices=OWNERSHIP_TYPES,
        max_length=20,
        null=True,
        blank=True,
        db_index=True,
    )
    business_type = models.CharField(
        choices=BUSINESS_TYPES,
        max_length=30,
        null=True,
        blank=True,
        help_text='Array(String(30))',
        db_index=True,
    )
    organization_logo = models.ForeignKey(
        Media,
        related_name='organization_logo_media',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='Integer',
        db_index=True)
    organization_banner = models.ForeignKey(
        Media,
        related_name='organization_banner_media',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='Integer',
        db_index=True)
    biography = models.TextField(max_length=700, blank=True, null=True, help_text='String(70)', db_index=True)
    description = models.TextField(blank=True, null=True, help_text='Text', max_length=1000, db_index=True)
    correspondence_language = ArrayField(models.CharField(max_length=50), blank=True, null=True, default=[],
                                         help_text='Array(String(50))', db_index=True)
    social_network = ArrayField(models.CharField(max_length=100), blank=True, null=True, default=[],
                                help_text='Array(String(100))', db_index=True)
    telegram_account = models.CharField(
        max_length=256, blank=True, null=True, db_index=True, help_text='String(256)')
    instagram_account = models.CharField(max_length=256, db_index=True, blank=True, null=True, help_text='String(256)')
    linkedin_account = models.CharField(max_length=256, db_index=True, blank=True, null=True, help_text='String(256)')
    staff_count = models.IntegerField(null=True, blank=True, help_text='تعداد پرسنل این سازمان که در سامانه حضور دارند را نمایش می دهد', db_index=True)
    active_flag = models.BooleanField(default=False, db_index=True)

    objects = BaseManager()

    def __str__(self):
        return str(self.pk) + ': ' + self.official_name

    def save(self, *args, **kwargs):
        from users.models import Identity
        with transaction.atomic():
            super(Organization, self).save(*args, **kwargs)
            if hasattr(self, 'identity'):
                identity = self.identity
            else:
                identity = Identity(identity_organization=self)
            identity.name = self.official_name
            identity.save()
            if self.staff_count:
                StaffCount.objects.create(identity_organization=self, staff_count=self.staff_count)


# Cache Model Data After Update
post_save.connect(update_cache, sender=Organization)
# Set Child Name
pre_save.connect(set_child_name, sender=Organization)


class StaffCount(Base):
    staff_count_organization = models.ForeignKey(Organization, related_name="staff_counts", db_index=True,
                                                 on_delete=models.CASCADE, help_text='Integer')
    count = models.IntegerField(help_text='Integer', db_index=True)

    def __str__(self):
        return '%s(%s)' % (self.staff_count_organization.official_name, self.count)


# Cache Model Data After Update
post_save.connect(update_cache, sender=StaffCount)
# Set Child Name
pre_save.connect(set_child_name, sender=StaffCount)


class OrganizationPicture(Base):
    picture_organization = models.ForeignKey(Organization, related_name="organization_pictures",
                                             on_delete=models.CASCADE, help_text='Integer', db_index=True)
    picture_media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name="organization_picture_media",
                                      help_text='Integer', db_index=True)
    order = models.IntegerField(default=0, help_text='Integer', db_index=True)
    description = models.TextField(blank=True, help_text='Text', db_index=True)

    def __str__(self):
        return self.picture_organization.official_name

    objects = BaseManager()


# Cache Model Data After Update
post_save.connect(update_cache, sender=OrganizationPicture)
# Set Child Name
pre_save.connect(set_child_name, sender=OrganizationPicture)


class Staff(Base):
    staff_organization = models.ForeignKey(Organization, related_name='staffs', db_index=True, on_delete=models.CASCADE,
                                           help_text='Integer')
    staff_user = models.ForeignKey(User, related_name='users', db_index=True, on_delete=models.CASCADE,
                                   help_text='Integer')

    position = models.CharField(max_length=50, db_index=True, help_text='String(50)')
    post_permission = models.BooleanField(default=False, help_text='Boolean', db_index=True)

    objects = BaseManager()


# Cache Model Data After Update
post_save.connect(update_cache, sender=Staff)
# Set Child Name
pre_save.connect(set_child_name, sender=Staff)


class Follow(Base):
    follow_followed = models.ForeignKey('users.Identity', related_name='followed', db_index=True,
                                        on_delete=models.CASCADE, help_text='Integer')
    follow_follower = models.ForeignKey('users.Identity', related_name='followers', db_index=True,
                                        on_delete=models.CASCADE, help_text='Integer')
    follow_accepted = models.BooleanField(default=False, db_index=True)

    objects = BaseManager()


# Cache Model Data After Update
post_save.connect(update_cache, sender=Follow)
# Set Child Name
pre_save.connect(set_child_name, sender=Follow)


class Ability(Base):
    ability_organization = models.ForeignKey(Organization, db_index=True, related_name='abilities',
                                             on_delete=models.CASCADE, help_text='Integer')
    title = models.CharField(max_length=50, db_index=True, help_text='String(50)')
    text = models.TextField(help_text='Text', db_index=True)

    objects = BaseManager()


# Cache Model Data After Update
post_save.connect(update_cache, sender=Ability)
# Set Child Name
pre_save.connect(set_child_name, sender=Ability)


class Confirmation(Base):
    confirmation_corroborant = models.ForeignKey('users.Identity', related_name='confirmation_corroborant',
                                                 db_index=True, on_delete=models.CASCADE, help_text='Integer')
    confirmation_confirmed = models.ForeignKey('users.Identity', related_name='confirmation_confirmed', db_index=True,
                                               on_delete=models.CASCADE, help_text='Integer', blank=True, null=True)
    title = models.CharField(max_length=50, db_index=True, help_text='String(String(50))')
    description = models.TextField(help_text='Text', db_index=True)
    link = models.CharField(max_length=200, help_text='String(200)', db_index=True)
    confirm_flag = models.BooleanField(default=False, help_text='Boolean', db_index=True)
    confirmation_parent = models.ForeignKey(Base, related_name='base_confirmation', db_index=True,
                                            on_delete=models.CASCADE, help_text='Integer')

    objects = BaseManager()


# Cache Model Data After Update
post_save.connect(update_cache, Confirmation)
# Set Child Name
pre_save.connect(set_child_name, sender=Confirmation)


class Customer(Base):
    customer_organization = models.ForeignKey(Organization, related_name='customer_organization', db_index=True,
                                              on_delete=models.CASCADE, help_text='Integer')
    related_customer = models.ForeignKey('users.Identity', related_name='customers', db_index=True,
                                         on_delete=models.CASCADE, help_text='Integer')
    title = models.CharField(max_length=100, db_index=True, help_text='String(100)')
    customer_picture = models.ForeignKey(Media, on_delete=models.CASCADE, help_text='Integer', db_index=True)
    customer_active = models.BooleanField(default=False, db_index=True)

    objects = BaseManager()


# Cache Model Data After Update
post_save.connect(update_cache, sender=Customer)
# Set Child Name
pre_save.connect(set_child_name, sender=Customer)


class MetaData(Base):
    META_TYPES = (
        ('phone', 'تولید کننده'),
        ('social', 'شبکه اجتماعی'),
        ('address', 'آدرس'),
    )
    meta_type = models.CharField(choices=META_TYPES, max_length=20, db_index=True)
    meta_title = models.CharField(max_length=20, blank=True, null=True, db_index=True)
    meta_value = models.CharField(max_length=255, db_index=True)
    meta_organization = models.ForeignKey(Organization, related_name='meta_data', blank=True, null=True,
                                          db_index=True, on_delete=models.CASCADE, help_text='Integer')


# Cache Model Data After Update
post_save.connect(update_cache, sender=MetaData)
# Set Child Name
pre_save.connect(set_child_name, sender=MetaData)
