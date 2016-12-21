# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-21 11:51
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20161220_1013'),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('urn', models.CharField(db_index=True, max_length=255)),
                ('la_name', models.CharField(blank=True, max_length=255, null=True)),
                ('school_name', models.CharField(blank=True, max_length=255, null=True)),
                ('school_type', models.CharField(blank=True, max_length=255, null=True)),
                ('school_capacity', models.IntegerField(null=True)),
                ('school_pupils', models.IntegerField(null=True)),
                ('postcode', models.CharField(blank=True, max_length=255, null=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(geography=True, srid=4326)),
            ],
        ),
    ]
