# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-12-19 12:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0012_auto_20171219_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='send_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 19, 16, 23, 22, 975042)),
        ),
    ]
