# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-12-27 15:00
from __future__ import unicode_literals

import danesh_boom.models.fields
from django.conf import settings
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='badge',
            name='create_time',
        ),
        migrations.AlterField(
            model_name='badge',
            name='badge_user',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='badges', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='badge',
            name='title',
            field=models.CharField(help_text='String(100)', max_length=100),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='certificate_user',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='certificates', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='picture_media',
            field=models.ForeignKey(blank=True, help_text='Integer', null=True, on_delete=django.db.models.deletion.SET_NULL, to='media.Media'),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='title',
            field=models.CharField(help_text='String(250)', max_length=250),
        ),
        migrations.AlterField(
            model_name='education',
            name='average',
            field=models.FloatField(blank=True, help_text='Float', null=True, validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='education',
            name='description',
            field=models.TextField(blank=True, help_text='Text'),
        ),
        migrations.AlterField(
            model_name='education',
            name='education_user',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='educations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='education',
            name='field_of_study',
            field=models.CharField(help_text='String(100)', max_length=100),
        ),
        migrations.AlterField(
            model_name='education',
            name='from_date',
            field=models.CharField(blank=True, help_text='String(7)', max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='education',
            name='grade',
            field=models.CharField(help_text='String(100)', max_length=100),
        ),
        migrations.AlterField(
            model_name='education',
            name='to_date',
            field=models.CharField(blank=True, help_text='String(7)', max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='education',
            name='university',
            field=models.CharField(help_text='String(100)', max_length=100),
        ),
        migrations.AlterField(
            model_name='identity',
            name='identity_organization',
            field=models.OneToOneField(blank=True, help_text='Integer', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='identity', to='organizations.Organization'),
        ),
        migrations.AlterField(
            model_name='identity',
            name='identity_user',
            field=models.OneToOneField(blank=True, help_text='Integer', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='identity', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='identity',
            name='name',
            field=models.CharField(help_text='String(150)', max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='birth_date',
            field=models.CharField(blank=True, help_text='String(10)', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='description',
            field=models.TextField(blank=True, help_text='Text'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='fax',
            field=danesh_boom.models.fields.PhoneField(blank=True, help_text='Phone', max_length=23),
        ),
        migrations.AlterField(
            model_name='profile',
            name='mobile',
            field=django.contrib.postgres.fields.ArrayField(base_field=danesh_boom.models.fields.PhoneField(max_length=23), blank=True, default=[], help_text='Array', size=None),
        ),
        migrations.AlterField(
            model_name='profile',
            name='national_code',
            field=models.CharField(blank=True, help_text='String(20)', max_length=20, validators=[django.core.validators.RegexValidator('^\\d{10}$')]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=django.contrib.postgres.fields.ArrayField(base_field=danesh_boom.models.fields.PhoneField(max_length=23), blank=True, default=[], help_text='Array', size=None),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_user',
            field=models.OneToOneField(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='public_email',
            field=models.EmailField(blank=True, help_text='Email', max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='telegram_account',
            field=models.CharField(blank=True, help_text='String(256)', max_length=256, validators=[django.core.validators.RegexValidator('^@[\\w\\d_]+$')]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='web_site',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(), blank=True, default=[], help_text='Array', size=None),
        ),
        migrations.AlterField(
            model_name='research',
            name='author',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, help_text='Array(String(100))', size=None),
        ),
        migrations.AlterField(
            model_name='research',
            name='page_count',
            field=models.IntegerField(blank=True, help_text='Integer', null=True),
        ),
        migrations.AlterField(
            model_name='research',
            name='publication',
            field=models.CharField(blank=True, help_text='String(100)', max_length=100),
        ),
        migrations.AlterField(
            model_name='research',
            name='research_user',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='researches', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='research',
            name='title',
            field=models.CharField(help_text='String(250)', max_length=250),
        ),
        migrations.AlterField(
            model_name='research',
            name='url',
            field=models.URLField(blank=True, help_text='URL'),
        ),
        migrations.AlterField(
            model_name='research',
            name='year',
            field=models.IntegerField(blank=True, help_text='Integer', null=True),
        ),
        migrations.AlterField(
            model_name='skill',
            name='description',
            field=models.TextField(blank=True, help_text='Text'),
        ),
        migrations.AlterField(
            model_name='skill',
            name='skill_user',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='skills', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='skill',
            name='tag',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, help_text='50', size=None),
        ),
        migrations.AlterField(
            model_name='skill',
            name='title',
            field=models.CharField(help_text='String(250)', max_length=250),
        ),
        migrations.AlterField(
            model_name='workexperience',
            name='from_date',
            field=models.CharField(blank=True, help_text='String(100)', max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='workexperience',
            name='name',
            field=models.CharField(blank=True, help_text='String(100)', max_length=100),
        ),
        migrations.AlterField(
            model_name='workexperience',
            name='position',
            field=models.CharField(blank=True, help_text='String(100)', max_length=100),
        ),
        migrations.AlterField(
            model_name='workexperience',
            name='status',
            field=models.CharField(choices=[('WITHOUT_CONFIRM', 'بدون تایید'), ('WAIT_FOR_CONFIRM', 'منتظر تایید'), ('CONFIRMED', 'تایید شده'), ('UNCONFIRMED', 'تایید نشده')], default='WITHOUT_CONFIRM', help_text='WITHOUT_CONFIRM | WAIT_FOR_CONFIRM | CONFIRMED | UNCONFIRMED', max_length=20),
        ),
        migrations.AlterField(
            model_name='workexperience',
            name='to_date',
            field=models.CharField(blank=True, help_text='String(7)', max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='workexperience',
            name='work_experience_organization',
            field=models.ForeignKey(blank=True, help_text='Integer', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='work_experience_organization', to='organizations.Organization'),
        ),
        migrations.AlterField(
            model_name='workexperience',
            name='work_experience_user',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='work_experiences', to=settings.AUTH_USER_MODEL),
        ),
    ]
