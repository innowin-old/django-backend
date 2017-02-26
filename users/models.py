from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator,\
    MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile",
                                on_delete=models.CASCADE)
    public_email = models.EmailField(null=True, blank=True)
    national_code = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    web_site = ArrayField(models.URLField(), blank=True, null=True)
    phone = ArrayField(models.CharField(max_length=20), blank=True, null=True)
    mobile = ArrayField(models.CharField(max_length=20), blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True)
    telegram_account = models.CharField(max_length=256, blank=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.user.username

    def clean(self):
        if self.birth_date and self.birth_date >= timezone.now().date():
            raise ValidationError(_('Invalid birth date'))


class Education(models.Model):
    user = models.ForeignKey(User, related_name="educations",
                             on_delete=models.CASCADE)
    grade = models.CharField(max_length=100)
    university = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    average = models.FloatField(
        validators=[
            MaxValueValidator(20),
            MinValueValidator(0)],
        null=True,
        blank=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return "%s(%s - %s)" % (
            self.user.username,
            self.grade,
            self.field_of_study
        )

    def clean(self):
        if self.from_date and self.to_date and self.from_date >= self.to_date:
            raise ValidationError(_('To date must be greather than from date'))


class Research(models.Model):
    user = models.ForeignKey(User, related_name="researches",
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    url = models.URLField(blank=True)
    author = ArrayField(models.CharField(max_length=100), blank=True)
    publication = models.CharField(max_length=100, blank=True)
    year = models.IntegerField(null=True, blank=True)
    page_count = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return "%s(%s)" % (self.user.username, self.title)


class Certificate(models.Model):
    user = models.ForeignKey(User, related_name="certificates",
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    picture = models.ImageField(upload_to='users/certificate/',
                                blank=True, null=True)

    def __unicode__(self):
        return "%s(%s)" % (self.user.username, self.title)


class WorkExperience(models.Model):
    user = models.ForeignKey(User, related_name="work_experiences",
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return "%s(%s)" % (self.user.username, self.name)

    def clean(self):
        if self.from_date and self.to_date and self.from_date >= self.to_date:
            raise ValidationError(_('To date must be greather than from date'))


class Skill(models.Model):
    user = models.ForeignKey(User, related_name="skills",
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    tag = ArrayField(models.CharField(max_length=50), blank=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return "%s(%s)" % (self.user.username, self.title)
