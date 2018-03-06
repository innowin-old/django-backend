from django.db import models
from django.db.models.signals import post_save, pre_save

from base.models import Base, BaseManager
from base.signals import update_cache, set_child_name
from media.models import Media


# Create your models here.
class Form(Base):
    title = models.CharField(max_length=50, db_index=True, help_text='String(50)')
    description = models.TextField(blank=True, db_index=True, help_text='Text')

    objects = BaseManager()


# Cache Model Data After Update
post_save.connect(update_cache, sender=Form)
# Set Child Name
pre_save.connect(set_child_name, sender=Form)


class Group(Base):
    title = models.CharField(max_length=50, db_index=True, help_text='String(50)')

    objects = BaseManager()


# Cache Model Data After Update
post_save.connect(update_cache, sender=Group)
# Set Child Name
pre_save.connect(set_child_name, sender=Group)


class FormGroup(Base):
    form_form = models.ForeignKey(Form, related_name="groups", db_index=True, help_text='Integer')
    form_group = models.ForeignKey(Group, related_name="form", db_index=True, help_text='Integer')
    required = models.BooleanField(default=False, help_text='Boolean')
    image = models.ForeignKey(Media, related_name="group_image", blank=True, null=True, help_text='Integer')

    objects = BaseManager()


# Cache Model Data After Update
post_save.connect(update_cache, sender=FormGroup)
# Set Child Name
pre_save.connect(set_child_name, sender=FormGroup)


class Element(Base):
    ELEMENTS = (
        ('text', 'txt'),
        ('number', 'num'),
    )
    name = models.CharField(choices=ELEMENTS, default="text", max_length=20, db_index=True, help_text='number | text')

    objects = BaseManager()


# Cache Model Data After Update
post_save.connect(update_cache, sender=Element)
# Set Child Name
pre_save.connect(set_child_name, sender=Element)


class FormGroupElement(models.Model):
    form_form_group = models.ForeignKey(FormGroup, related_name="form_form_group", help_text='Integer')
    form_element = models.ForeignKey(Element, related_name="form_element", help_text='Integer')

    objects = BaseManager()


# Cache Model Data After Update
post_save.connect(update_cache, sender=FormGroupElement)
# Set Child Name
pre_save.connect(set_child_name, sender=FormGroupElement)


class Data(Base):
    form_group_element = models.ForeignKey(FormGroupElement, related_name="form_group_element", db_index=True,
                                           help_text='Integer')
    amount = models.TextField(blank=True, db_index=True, help_text='Text')

    objects = BaseManager()


# Cache Model Data After Update
post_save.connect(update_cache, sender=Data)
# Set Child Name
pre_save.connect(set_child_name, sender=Data)
