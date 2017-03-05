from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator,\
    MinValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

import re


class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile",
                                on_delete=models.CASCADE)
    public_email = models.EmailField(null=True, blank=True)
    national_code = models.CharField(max_length=20, blank=True,
                                     validators=[RegexValidator('^\d{10}$')])
    birth_date = models.CharField(max_length=10, blank=True, null=True)
    web_site = ArrayField(models.URLField(), blank=True, null=True)
    phone = ArrayField(
        models.CharField(
            max_length=20,
            validators=[
                RegexValidator('^\+\d{1,3}-\d{2,3}-\d{3,14}$')]),
        blank=True,
        null=True)
    mobile = ArrayField(
        models.CharField(
            max_length=20,
            validators=[
                RegexValidator('^\+\d{1,3}-\d{2,3}-\d{3,14}$')]),
        blank=True,
        null=True)
    fax = models.CharField(
        max_length=20,
        validators=[
            RegexValidator('^\+\d{1,3}-\d{2,3}-\d{3,14}$')],
        blank=True)
    telegram_account = models.CharField(
        max_length=256, blank=True, validators=[
            RegexValidator('^@[\w\d_]+$')])
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.user.username

    def clean(self):
        if self.birth_date:
            p = re.compile('^\d{4}-\d{2}-\d{2}$')
            birth_date = self.birth_date
            if not re.match(p, birth_date):
                raise ValidationError(_('Invalid birth date'))
            now = timezone.now().date().strftime('%Y-%m-%d')
            if birth_date > now:
                raise ValidationError(_('Invalid birth date'))


class Education(models.Model):
    user = models.ForeignKey(User, related_name="educations",
                             on_delete=models.CASCADE)
    grade = models.CharField(max_length=100)
    university = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    from_date = models.CharField(max_length=7, blank=True, null=True)
    to_date = models.CharField(max_length=7, blank=True, null=True)
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
    from_date = models.CharField(max_length=7, blank=True, null=True)
    to_date = models.CharField(max_length=7, blank=True, null=True)

    def __unicode__(self):
        return "%s(%s)" % (self.user.username, self.name)

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
            raise ValidationError(_('To date must be greather than from date'))


class Skill(models.Model):
    user = models.ForeignKey(User, related_name="skills",
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    tag = ArrayField(models.CharField(max_length=50), blank=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return "%s(%s)" % (self.user.username, self.title)
