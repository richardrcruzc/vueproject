# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-04-09 22:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_auto_20180409_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='level',
            field=models.IntegerField(default=0),
        ),
    ]