# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-19 11:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0038_auto_20170118_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='overheadline',
            name='gdo_gid',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
