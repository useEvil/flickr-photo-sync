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
            name='DbMaintenance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('exported_file', models.FileField(default=b'', upload_to=b'', blank=True)),
                ('imported_file', models.FileField(default=b'', upload_to=b'', blank=True)),
                ('to_db', models.CharField(blank=True, max_length=25, choices=[(b'default', b'default')])),
                ('from_db', models.CharField(blank=True, max_length=25, choices=[(b'default', b'default')])),
                ('backed_up', models.BooleanField(default=True, verbose_name=b'Back Up First')),
                ('description', models.TextField(default=b'', null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='dbmaintenance_created_by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='dbmaintenance_modified_by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
