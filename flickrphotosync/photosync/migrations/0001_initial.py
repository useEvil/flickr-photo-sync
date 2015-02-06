# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=250)),
                ('slug', models.CharField(max_length=250)),
                ('total', models.PositiveIntegerField(default=0)),
                ('page', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=65000, null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='collection_created_by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='collection_modified_by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CopySettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('slug', models.CharField(max_length=250)),
                ('full_path', models.CharField(max_length=1000)),
                ('last_photo', models.PositiveIntegerField(default=0)),
                ('last_moive', models.PositiveIntegerField(default=0)),
                ('photo_name_format', models.CharField(max_length=100)),
                ('movie_name_format', models.CharField(max_length=100)),
                ('counter', models.PositiveIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=250)),
                ('slug', models.CharField(max_length=250)),
                ('file_name', models.CharField(max_length=500)),
                ('full_path', models.CharField(max_length=1000)),
                ('width', models.PositiveIntegerField(default=0)),
                ('height', models.PositiveIntegerField(default=0)),
                ('type', models.PositiveIntegerField(default=0, choices=[(0, b'JPG'), (1, b'GIF'), (2, b'PNG'), (3, b'TIFF')])),
                ('farm', models.PositiveIntegerField(default=0)),
                ('server', models.PositiveIntegerField(default=0)),
                ('description', models.TextField(max_length=65000, null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='photo_created_by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='photo_modified_by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhotoSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=250)),
                ('slug', models.CharField(max_length=250)),
                ('full_path', models.CharField(max_length=1000)),
                ('total', models.PositiveIntegerField(default=0)),
                ('farm', models.PositiveIntegerField(default=0)),
                ('server', models.PositiveIntegerField(default=0)),
                ('primary', models.PositiveIntegerField(default=0)),
                ('description', models.TextField(max_length=65000, null=True, blank=True)),
                ('collection', models.ForeignKey(related_name='photosets', blank=True, to='photosync.Collection', null=True)),
                ('created_by', models.ForeignKey(related_name='photoset_created_by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='photoset_modified_by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='photo',
            name='photoset',
            field=models.ForeignKey(related_name='photos', to='photosync.PhotoSet'),
            preserve_default=True,
        ),
    ]
