# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-22 14:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0003_episode_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='length',
            field=models.DurationField(),
        ),
    ]
