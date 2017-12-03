# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-07 14:02
from __future__ import unicode_literals

import danesh_boom.models.fields
from django.conf import settings
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('media', '0001_initial'),
        ('organizations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('badge', models.CharField(max_length=100)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='badges', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('picture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='media.Media')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificates', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(max_length=100)),
                ('university', models.CharField(max_length=100)),
                ('field_of_study', models.CharField(max_length=100)),
                ('from_date', models.CharField(blank=True, max_length=7, null=True)),
                ('to_date', models.CharField(blank=True, max_length=7, null=True)),
                ('average', models.FloatField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(0)])),
                ('description', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='educations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Identity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('organization', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='identity', to='organizations.Organization')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='identity', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('national_code', models.CharField(blank=True, max_length=20, validators=[django.core.validators.RegexValidator('^\\d{10}$')])),
                ('birth_date', models.CharField(blank=True, max_length=10, null=True)),
                ('web_site', django.contrib.postgres.fields.ArrayField(base_field=models.URLField(), blank=True, default=[], size=None)),
                ('phone', django.contrib.postgres.fields.ArrayField(base_field=danesh_boom.models.fields.PhoneField(max_length=23), blank=True, default=[], size=None)),
                ('mobile', django.contrib.postgres.fields.ArrayField(base_field=danesh_boom.models.fields.PhoneField(max_length=23), blank=True, default=[], size=None)),
                ('fax', danesh_boom.models.fields.PhoneField(blank=True, max_length=23)),
                ('telegram_account', models.CharField(blank=True, max_length=256, validators=[django.core.validators.RegexValidator('^@[\\w\\d_]+$')])),
                ('description', models.TextField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Research',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('url', models.URLField(blank=True)),
                ('author', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, size=None)),
                ('publication', models.CharField(blank=True, max_length=100)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('page_count', models.IntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='researches', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('tag', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, size=None)),
                ('description', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WorkExperience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('position', models.CharField(blank=True, max_length=100)),
                ('from_date', models.CharField(blank=True, max_length=7, null=True)),
                ('to_date', models.CharField(blank=True, max_length=7, null=True)),
                ('status', models.CharField(choices=[('WITHOUT_CONFIRM', 'بدون تایید'), ('WAIT_FOR_CONFIRM', 'منتظر تایید'), ('CONFIRMED', 'تایید شده'), ('UNCONFIRMED', 'تایید نشده')], default='WITHOUT_CONFIRM', max_length=20)),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='work_experience_organization', to='organizations.Organization')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='work_experiences', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='badge',
            unique_together=set([('user', 'badge')]),
        ),
    ]
