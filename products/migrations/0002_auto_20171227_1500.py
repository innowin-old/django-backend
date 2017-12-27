# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-12-27 15:00
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='create_time',
        ),
        migrations.RemoveField(
            model_name='price',
            name='create_time',
        ),
        migrations.AlterField(
            model_name='category',
            name='category_parent',
            field=models.ForeignKey(blank=True, help_text='Integer', null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='creatable',
            field=models.BooleanField(default=False, help_text='Boolean'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, help_text='String(100)', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(db_index=True, help_text='String(100)', max_length=100),
        ),
        migrations.AlterField(
            model_name='categoryfield',
            name='field_category',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='category_fields', to='products.Category'),
        ),
        migrations.AlterField(
            model_name='categoryfield',
            name='name',
            field=models.CharField(db_index=True, help_text='String(100)', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='categoryfield',
            name='option',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, db_index=True, help_text='JSON', null=True),
        ),
        migrations.AlterField(
            model_name='categoryfield',
            name='order',
            field=models.IntegerField(db_index=True, default=0, help_text='Integer'),
        ),
        migrations.AlterField(
            model_name='categoryfield',
            name='title',
            field=models.CharField(db_index=True, help_text='String(100)', max_length=100),
        ),
        migrations.AlterField(
            model_name='categoryfield',
            name='type',
            field=models.CharField(choices=[('string', 'ارزش آن بصورت استرینگ پر شود'), ('float', 'ارزش آن بصورت عدد پر شود'), ('choices', 'ارائه ارزش بصورت انتخابی'), ('bool', 'ارئه ارزش بصورت چک باکس')], db_index=True, default='string', help_text='string | float | choices | bool', max_length=50),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_product',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='product_comments', to='products.Product'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_user',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='user_product_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(db_index=True, help_text='Text'),
        ),
        migrations.AlterField(
            model_name='picture',
            name='description',
            field=models.TextField(blank=True, db_index=True, help_text='Text'),
        ),
        migrations.AlterField(
            model_name='picture',
            name='order',
            field=models.IntegerField(default=0, help_text='Integer'),
        ),
        migrations.AlterField(
            model_name='picture',
            name='picture_media',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='product_picture_media', to='media.Media'),
        ),
        migrations.AlterField(
            model_name='picture',
            name='picture_product',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='product_pictures', to='products.Product'),
        ),
        migrations.AlterField(
            model_name='price',
            name='price_product',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='products.Product'),
        ),
        migrations.AlterField(
            model_name='price',
            name='value',
            field=models.FloatField(help_text='Float'),
        ),
        migrations.AlterField(
            model_name='product',
            name='attrs',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='JSON', null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='city',
            field=models.CharField(blank=True, db_index=True, help_text='String(50)', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='country',
            field=models.CharField(db_index=True, help_text='String(50)', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='custom_attrs',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='JSON', null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, db_index=True, help_text='String(1000)', max_length=1000),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(db_index=True, help_text='String(100)', max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_category',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.Category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_owner',
            field=models.ForeignKey(help_text='Integer', on_delete=django.db.models.deletion.CASCADE, related_name='identity_products', to='users.Identity'),
        ),
        migrations.AlterField(
            model_name='product',
            name='province',
            field=models.CharField(db_index=True, help_text='String(50)', max_length=50),
        ),
    ]
