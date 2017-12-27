# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-12-27 15:00
from __future__ import unicode_literals

import danesh_boom.models.fields
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_auto_20171218_0717'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='create_time',
        ),
        migrations.RemoveField(
            model_name='staffcount',
            name='create_time',
        ),
        migrations.AlterField(
            model_name='ability',
            name='ability_organization',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='abilities', to='organizations.Organization'),
        ),
        migrations.AlterField(
            model_name='ability',
            name='text',
            field=models.TextField(help_text='Text'),
        ),
        migrations.AlterField(
            model_name='ability',
            name='title',
            field=models.CharField(help_text='String(50)', max_length=50),
        ),
        migrations.AlterField(
            model_name='confirmation',
            name='confirm_flag',
            field=models.BooleanField(default=False, help_text='Boolean'),
        ),
        migrations.AlterField(
            model_name='confirmation',
            name='confirmation_confirmed',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='confirmation_confirmaed', to='users.Identity'),
        ),
        migrations.AlterField(
            model_name='confirmation',
            name='confirmation_corroborant',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='confirmation_corroborant', to='users.Identity'),
        ),
        migrations.AlterField(
            model_name='confirmation',
            name='description',
            field=models.TextField(help_text='Text'),
        ),
        migrations.AlterField(
            model_name='confirmation',
            name='link',
            field=models.CharField(help_text='String(200)', max_length=200),
        ),
        migrations.AlterField(
            model_name='confirmation',
            name='title',
            field=models.CharField(help_text='String(String(50))', max_length=50),
        ),
        migrations.AlterField(
            model_name='customer',
            name='customer_organization',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='customer_organization', to='organizations.Organization'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='customer_picture',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, to='media.Media'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='related_customer',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='customers', to='users.Identity'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='title',
            field=models.CharField(help_text='String(100)', max_length=100),
        ),
        migrations.AlterField(
            model_name='follow',
            name='follow_follower',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='following', to='users.Identity'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='follow_identity',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='users.Identity'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='address',
            field=models.TextField(blank=True, help_text='Text'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='admins',
            field=models.ManyToManyField(blank=True, help_text='Integer', related_name='organization_admins', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='organization',
            name='biography',
            field=models.TextField(blank=True, help_text='String(256)', max_length=256),
        ),
        migrations.AlterField(
            model_name='organization',
            name='business_type',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('producer', 'تولید کننده'), ('investor', 'سرمایه گذار'), ('service provider', 'ارائه دهنده خدمات')], help_text='Array(String(30))', max_length=30), size=None),
        ),
        migrations.AlterField(
            model_name='organization',
            name='city',
            field=models.CharField(help_text='String(50)', max_length=50),
        ),
        migrations.AlterField(
            model_name='organization',
            name='correspondence_language',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, default=[], help_text='Array(String(50))', size=None),
        ),
        migrations.AlterField(
            model_name='organization',
            name='country',
            field=models.CharField(help_text='String(50)', max_length=50),
        ),
        migrations.AlterField(
            model_name='organization',
            name='description',
            field=models.TextField(blank=True, help_text='Text'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='established_year',
            field=models.IntegerField(blank=True, help_text='Integer', null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='national_code',
            field=models.CharField(help_text='String(20)', max_length=20),
        ),
        migrations.AlterField(
            model_name='organization',
            name='nike_name',
            field=models.CharField(blank=True, help_text='String(100)', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='official_name',
            field=models.CharField(help_text='String(75)', max_length=75),
        ),
        migrations.AlterField(
            model_name='organization',
            name='organization_logo',
            field=models.ForeignKey(blank=True, help_text='Integer', null=True, on_delete=django.db.models.deletion.SET_NULL, to='media.Media'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='owner',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='organizations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='organization',
            name='phone',
            field=django.contrib.postgres.fields.ArrayField(base_field=danesh_boom.models.fields.PhoneField(max_length=23), blank=True, default=[], help_text='Phone', size=None),
        ),
        migrations.AlterField(
            model_name='organization',
            name='province',
            field=models.CharField(help_text='String(50)', max_length=50),
        ),
        migrations.AlterField(
            model_name='organization',
            name='registrar_organization',
            field=models.CharField(blank=True, help_text='String(100)', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='registration_ads_url',
            field=models.URLField(blank=True, help_text='URL', null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='social_network',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, default=[], help_text='Array(String(100))', size=None),
        ),
        migrations.AlterField(
            model_name='organization',
            name='staff_count',
            field=models.IntegerField(blank=True, help_text='Integer', null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='username',
            field=models.CharField(help_text='String(100)', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='web_site',
            field=models.URLField(blank=True, help_text='URL', null=True),
        ),
        migrations.AlterField(
            model_name='organizationpicture',
            name='description',
            field=models.TextField(blank=True, help_text='Text'),
        ),
        migrations.AlterField(
            model_name='organizationpicture',
            name='order',
            field=models.IntegerField(default=0, help_text='Integer'),
        ),
        migrations.AlterField(
            model_name='organizationpicture',
            name='picture_media',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='organization_picture_media', to='media.Media'),
        ),
        migrations.AlterField(
            model_name='organizationpicture',
            name='picture_organization',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='organization_pictures', to='organizations.Organization'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_organization',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='organizations.Organization'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_picture',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, to='media.Media'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_user',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='user_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(help_text='Text'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(help_text='String(100)', max_length=100),
        ),
        migrations.AlterField(
            model_name='post',
            name='type',
            field=models.CharField(choices=[('post', 'پست'), ('offer', 'تقاضا'), ('request', 'عرضه')], help_text='post | offer | request', max_length=10),
        ),
        migrations.AlterField(
            model_name='staff',
            name='position',
            field=models.CharField(help_text='String(50)', max_length=50),
        ),
        migrations.AlterField(
            model_name='staff',
            name='post_permission',
            field=models.BooleanField(default=False, help_text='Boolean'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_organization',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='staffs', to='organizations.Organization'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_user',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='staffcount',
            name='count',
            field=models.IntegerField(help_text='Integer'),
        ),
        migrations.AlterField(
            model_name='staffcount',
            name='staff_count_organization',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='staff_counts', to='organizations.Organization'),
        ),
    ]
