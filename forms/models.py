from django.db import models

from base.models import Base
from media.models import Media

# Create your models here.
class Form(Base):
    title = models.CharField(max_length=50, db_index=True)
    description = models.TextField(blank=True, db_index=True)


class Group(Base):
    title = models.CharField(max_length=50, db_index=True)


class FormGroup(Base):
    form_form = models.ForeignKey(Form, related_name="groups", db_index=True)
    form_group = models.ForeignKey(Group, related_name="form", db_index=True)
    required = models.BooleanField(default=False)
    image = models.ForeignKey(Media, related_name="group_image", blank=True, null=True)


class Element(Base):
    ELEMENTS = (
        ('text', 'txt'),
        ('number', 'num'),
    )
    name = models.CharField(choices=ELEMENTS, default="text", max_length=20, db_index=True)


class FormGroupElement(models.Model):
    form_form_group = models.ForeignKey(FormGroup, related_name="form_form_group")
    form_element = models.ForeignKey(Element, related_name="form_element")


class Data(models.Model):
    form_group_element = models.ForeignKey(FormGroupElement, related_name="form_group_element", db_index=True)
    amount = models.TextField(blank=True, db_index=True)