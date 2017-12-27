from django.db import models

from base.models import Base
from media.models import Media

# Create your models here.
class Form(Base):
    title = models.CharField(max_length=50, db_index=True, help_text='String(50)')
    description = models.TextField(blank=True, db_index=True, help_text='Text')


class Group(Base):
    title = models.CharField(max_length=50, db_index=True, help_text='String(50)')


class FormGroup(Base):
    form_form = models.ForeignKey(Form, related_name="groups", db_index=True, help_text='Integer')
    form_group = models.ForeignKey(Group, related_name="form", db_index=True, help_text='Integer')
    required = models.BooleanField(default=False, help_text='Boolean')
    image = models.ForeignKey(Media, related_name="group_image", blank=True, null=True, help_text='Integer')


class Element(Base):
    ELEMENTS = (
        ('text', 'txt'),
        ('number', 'num'),
    )
    name = models.CharField(choices=ELEMENTS, default="text", max_length=20, db_index=True, help_text='number | text')


class FormGroupElement(models.Model):
    form_form_group = models.ForeignKey(FormGroup, related_name="form_form_group", help_text='Integer')
    form_element = models.ForeignKey(Element, related_name="form_element", help_text='Integer')


class Data(models.Model):
    form_group_element = models.ForeignKey(FormGroupElement, related_name="form_group_element", db_index=True, help_text='Integer')
    amount = models.TextField(blank=True, db_index=True, help_text='Text')