# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-20 07:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20170319_0804'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificate',
            name='picture',
        ),
    ]
