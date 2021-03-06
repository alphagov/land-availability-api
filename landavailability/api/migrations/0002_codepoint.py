# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-22 13:50
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodePoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postcode', models.CharField(db_index=True, max_length=20)),
                ('quality', models.IntegerField()),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('country', models.CharField(db_index=True, max_length=24)),
                ('nhs_region', models.CharField(db_index=True, max_length=24)),
                ('nhs_health_authority', models.CharField(db_index=True, max_length=24)),
                ('county', models.CharField(db_index=True, max_length=24)),
                ('district', models.CharField(db_index=True, max_length=24)),
                ('ward', models.CharField(db_index=True, max_length=24)),
            ],
        ),
    ]
