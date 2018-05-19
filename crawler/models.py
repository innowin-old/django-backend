from django.db import models


# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=100)


class ResearchGateTopic(models.Model):
    name = models.CharField(max_length=100)
    delete_flag = models.BooleanField(default=False)


class VitrinOrganization(models.Model):
    internal_link = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    telegram_link = models.CharField(max_length=255, blank=True, null=True)
    instagram_link = models.CharField(max_length=255, blank=True, null=True)