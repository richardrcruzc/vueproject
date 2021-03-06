# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-08-16 07:43
from __future__ import unicode_literals

import arcutils.path
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_auto_20190731_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readingfile',
            name='path',
            field=models.FileField(upload_to=arcutils.path.UploadToPathAndRename('files\\2019\\08')),
        ),
        migrations.AlterField(
            model_name='readingquestion',
            name='tutorial_file',
            field=models.FileField(blank=True, null=True, upload_to=arcutils.path.UploadToPathAndRename('files/tutorial\\2019\\08')),
        ),
    ]
