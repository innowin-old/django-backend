from django.db import models, transaction
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

from danesh_boom.models import PhoneField
from media.models import Media
from base.models import Base, BaseManager
from base.signals import update_cache


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
                              on_delete=models.CASCADE, help_text='Integer')
    admins = models.ManyToManyField(User,
                                    related_name="organization_admins",
                                    blank=True,
                                    help_text='Integer')
    username = models.CharField(max_length=100, unique=True, help_text='String(100)')
    nike_name = models.CharField(max_length=100, db_index=True, null=True, blank=True, help_text='String(100)')
    official_name = models.CharField(max_length=75, db_index=True, help_text='String(75)')
    national_code = models.CharField(max_length=20, db_index=True, help_text='String(20)')
    registration_ads_url = models.URLField(db_index=True, null=True, blank=True, help_text='URL')
    registrar_organization = models.CharField(max_length=100, db_index=True, null=True, blank=True, help_text='String(100)')
    country = models.CharField(max_length=50, db_index=True, help_text='String(50)')
    province = models.CharField(max_length=50, db_index=True, help_text='String(50)')
    city = models.CharField(max_length=50, db_index=True, help_text='String(50)')
    address = models.TextField(blank=True, db_index=True, help_text='Text')
    phone = ArrayField(PhoneField(), blank=True, db_index=True, default=[], help_text='Phone')
    web_site = models.URLField(null=True, db_index=True, blank=True, help_text='URL')
    established_year = models.IntegerField(null=True, db_index=True, blank=True, help_text='Integer')
    ownership_type = models.CharField(
        choices=OWNERSHIP_TYPES,
        max_length=20)
    business_type = ArrayField(models.CharField(
        choices=BUSINESS_TYPES,
        max_length=30,
        help_text='Array(String(30))')
    )
    organization_logo = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='Integer')
    biography = models.TextField(max_length=256, blank=True, help_text='String(256)')
    description = models.TextField(blank=True, help_text='Text')
    correspondence_language = ArrayField(models.CharField(max_length=50), blank=True, default=[], help_text='Array(String(50))')
    social_network = ArrayField(models.CharField(max_length=100), blank=True, default=[], help_text='Array(String(100))')
    staff_count = models.IntegerField(null=True, blank=True, help_text='Integer')

    objects = BaseManager()

    def __str__(self):
        return self.official_name

    def save(self, *args, **kwargs):
        from users.models import Identity
        with transaction.atomic():
            super(Organization, self).save(*args, **kwargs)
            if hasattr(self, 'identity'):
                identity = self.identity
            else:
                identity = Identity(organization=self)
            identity.name = self.official_name
            identity.save()
            if self.staff_count:
                StaffCount.objects.create(organization=self, count=self.staff_count)


# Cache Model Data After Update
post_save.connect(update_cache, sender=Organization)


class StaffCount(Base):
    staff_count_organization = models.ForeignKey(Organization, related_name="staff_counts", db_index=True,
                                     on_delete=models.CASCADE, help_text='Integer')
    count = models.IntegerField(help_text='Integer')

    def __str__(self):
        return '%s(%s)' % (self.staff_count_organization.official_name, self.count)


class OrganizationPicture(Base):
    picture_organization = models.ForeignKey(Organization, related_name="organization_pictures",
                                     on_delete=models.CASCADE, help_text='Integer')
    picture_media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name="organization_picture_media", help_text='Integer')
    order = models.IntegerField(default=0, help_text='Integer')
    description = models.TextField(blank=True, help_text='Text')

    def __str__(self):
        return self.picture_organization.official_name

    objects = BaseManager()


# Cache Model Data After Update
post_save.connect(update_cache, sender=OrganizationPicture)


class Staff(Base):
    staff_organization = models.ForeignKey(Organization, related_name='staffs', db_index=True, on_delete=models.CASCADE, help_text='Integer')
    staff_user = models.ForeignKey(User, related_name='users', db_index=True, on_delete=models.CASCADE, help_text='Integer')

    position = models.CharField(max_length=50, db_index=True, help_text='String(50)')
    post_permission = models.BooleanField(default=False, help_text='Boolean')

    objects = BaseManager()


# Cache Model Data After Update
post_save.connect(update_cache, sender=Staff)


class Follow(Base):
    follow_identity = models.ForeignKey('users.Identity', related_name='followers', db_index=True, on_delete=models.CASCADE, help_text='Integer')
    follow_follower = models.ForeignKey('users.Identity', related_name='following', db_index=True, on_delete=models.CASCADE, help_text='Integer')

    objects = BaseManager()


# Cache Model Data After Update
post_save.connect(update_cache, sender=Follow)


class Ability(Base):
    ability_organization = models.ForeignKey(Organization, db_index=True, related_name='abilities', on_delete=models.CASCADE, help_text='Integer')
    title = models.CharField(max_length=50, db_index=True, help_text='String(50)')
    text = models.TextField(help_text='Text', db_index=True)

    objects = BaseManager()


# Cache Model Data After Update
post_save.connect(update_cache, sender=Ability)


class Confirmation(Base):
    confirmation_corroborant = models.ForeignKey('users.Identity', related_name='confirmation_corroborant', db_index=True, on_delete=models.CASCADE, help_text='Integer')
    confirmation_confirmed = models.ForeignKey('users.Identity', related_name='confirmation_confirmaed', db_index=True, on_delete=models.CASCADE, help_text='Integer')
    title = models.CharField(max_length=50, db_index=True, help_text='String(String(50))')
    description = models.TextField(help_text='Text')
    link = models.CharField(max_length=200, help_text='String(200)')
    confirm_flag = models.BooleanField(default=False, help_text='Boolean')

    objects = BaseManager()


# Cache Model Data After Update
post_save.connect(update_cache, Confirmation)


class Customer(Base):
    customer_organization = models.ForeignKey(Organization, related_name='customer_organization', db_index=True, on_delete=models.CASCADE, help_text='Integer')
    related_customer = models.ForeignKey('users.Identity', related_name='customers', db_index=True, on_delete=models.CASCADE, help_text='Integer')
    title = models.CharField(max_length=100, db_index=True, help_text='String(100)')
    customer_picture = models.ForeignKey(Media, on_delete=models.CASCADE, help_text='Integer')

    objects = BaseManager()


# Cache Model Data After Update
post_save.connect(update_cache, sender=Customer)