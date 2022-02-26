# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-07-31 14:36
from __future__ import unicode_literals

import arcutils.path
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_readingquestion_tutorial_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readingquestion',
            name='tutorial_file',
            field=models.FileField(blank=True, null=True, upload_to=arcutils.path.UploadToPathAndRename('files/tutorial/2019/07')),
        ),
    ]
