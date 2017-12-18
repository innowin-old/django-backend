from django.db import models, transaction
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

from media.models import Media
from danesh_boom.models import PhoneField
from base.models import Base


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

    owner = models.ForeignKey(User, related_name="organizations",
                              on_delete=models.CASCADE)
    admins = models.ManyToManyField(User,
                                    related_name="organization_admins",
                                    blank=True)
    username = models.CharField(max_length=100, unique=True)
    nike_name = models.CharField(max_length=100, null=True, blank=True)
    official_name = models.CharField(max_length=75)
    national_code = models.CharField(max_length=20)
    registration_ads_url = models.URLField(null=True, blank=True)
    registrar_organization = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.TextField(blank=True)
    phone = ArrayField(PhoneField(), blank=True, default=[])
    web_site = models.URLField(null=True, blank=True)
    established_year = models.IntegerField(null=True, blank=True)
    ownership_type = models.CharField(
        choices=OWNERSHIP_TYPES,
        max_length=20)
    business_type = ArrayField(models.CharField(
        choices=BUSINESS_TYPES,
        max_length=30)
    )
    organization_logo = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    biography = models.TextField(max_length=256, blank=True)
    description = models.TextField(blank=True)
    correspondence_language = ArrayField(models.CharField(max_length=50), blank=True, default=[])
    social_network = ArrayField(models.CharField(max_length=100), blank=True, default=[])
    staff_count = models.IntegerField(null=True, blank=True)

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


class StaffCount(Base):
    staff_count_organization = models.ForeignKey(Organization, related_name="staff_counts",
                                     on_delete=models.CASCADE)
    count = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s(%s)' % (self.organization.official_name, self.count)


class OrganizationPicture(Base):
    picture_organization = models.ForeignKey(Organization, related_name="organization_pictures",
                                     on_delete=models.CASCADE)
    picture_media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name="organization_picture_media")
    order = models.IntegerField(default=0)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.organization.official_name


class Post(Base):
    POST_TYPES = (
        ('post', 'پست'),
        ('offer', 'تقاضا'),
        ('request', 'عرضه')
    )
    post_organization = models.ForeignKey(Organization, related_name="posts", on_delete=models.CASCADE)
    post_user = models.ForeignKey(User, related_name="user_posts", on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    text = models.TextField()
    type = models.CharField(choices=POST_TYPES, max_length=10)
    post_picture = models.ForeignKey(Media, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    @property
    def user_username(self):
        return self.user.username


class Staff(Base):
    staff_organization = models.ForeignKey(Organization, related_name='staffs', on_delete=models.CASCADE)
    staff_user = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)

    position = models.CharField(max_length=50)
    post_permission = models.BooleanField(default=False)


class Follow(Base):
    follow_identity = models.ForeignKey('users.Identity', related_name='followers', on_delete=models.CASCADE)
    follow_follower = models.ForeignKey('users.Identity', related_name='following', on_delete=models.CASCADE)


class Ability(Base):
    ability_organization = models.ForeignKey(Organization, related_name='abilities', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField()


class Confirmation(Base):
    confirmation_corroborant = models.ForeignKey('users.Identity', related_name='confirmation_corroborant', on_delete=models.CASCADE)
    confirmation_confirmed = models.ForeignKey('users.Identity', related_name='confirmation_confirmaed', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    link = models.CharField(max_length=200)
    confirm_flag = models.BooleanField(default=False)


class Customer(Base):
    customer_organization = models.ForeignKey(Organization, related_name='customer_organization', on_delete=models.CASCADE)
    related_customer = models.ForeignKey('users.Identity', related_name='customers', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    customer_picture = models.ForeignKey(Media, on_delete=models.CASCADE)
