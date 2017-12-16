# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-12-16 11:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0002_auto_20171216_0620'),
        ('users', '0001_initial'),
        ('organizations', '0004_confirmation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('picture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='media.Media')),
                ('related_customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customers', to='users.Identity')),
            ],
        ),
    ]
