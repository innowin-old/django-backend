from django.db import models, transaction
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField

from media.models import Media
from danesh_boom.models import PhoneField


class Organization(models.Model):
    OWNERSHIP_TYPES = (
        ('idi', 'موسسه انفرادی'),
        ('org', 'شرکت'),
        ('cop', 'تعاونی'),
        ('pvt', 'سهامی خاص'),
        ('llp', 'سهامی عام'),
        ('gco', 'شرکت دولتی'),
        ('oth', 'سایر'),
    )

    user = models.ForeignKey(User, related_name="organizations",
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    organ_name = models.CharField(max_length=75)
    national_code = models.CharField(max_length=20)
    registration_ads_url = models.URLField(blank=True)
    registrar_organization = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    phone = ArrayField(PhoneField(), blank=True, null=True)
    web_site = models.URLField(blank=True)
    established_year = models.IntegerField(null=True, blank=True)
    ownership_type = models.CharField(
        choices=OWNERSHIP_TYPES,
        max_length=20,
        default='oth')
    business_type = ArrayField(models.CharField(max_length=100))
    logo = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        blank=True,
        null=True)
    description = models.TextField(blank=True)
    advantages = models.TextField(blank=True)
    correspondence_language = ArrayField(
        models.CharField(max_length=50), blank=True)
    telegram_channel = models.CharField(
        max_length=256, blank=True, validators=[
            RegexValidator('^@[\w\d_]+$')])

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        from users.models import Identity
        with transaction.atomic():
            super(Organization, self).save(*args, **kwargs)
            if hasattr(self, 'identity'):
                identity = self.identity
            else:
                identity = Identity(organization=self)
            identity.name = self.organ_name
            identity.save()


class StaffCount(models.Model):
    organization = models.ForeignKey(Organization, related_name="staff_counts",
                                     on_delete=models.CASCADE)
    count = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s(%s)' % (self.organization.name, self.count)


class Picture(models.Model):
    organization = models.ForeignKey(Organization, related_name="pictures",
                                     on_delete=models.CASCADE)
    picture = models.ForeignKey(Media, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.organization.name


class UserAgent(models.Model):
    organization = models.ForeignKey(Organization, related_name="user_agents",
                                     on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="user_organizations",
                             on_delete=models.CASCADE)
    agent_subject = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = (('organization', 'user'),)

    def __str__(self):
        return '%s(%s)' % (self.organization.name, self.user.username)
