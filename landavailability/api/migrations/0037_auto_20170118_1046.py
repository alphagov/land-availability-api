# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-18 10:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_auto_20170117_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='motorway',
            name='identifier',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
