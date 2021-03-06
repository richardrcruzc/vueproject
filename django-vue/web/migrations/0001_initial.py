# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-12 09:55
from __future__ import unicode_literals

import arcutils.path
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
                ('is_correct', models.BooleanField(default=False)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'question_choice',
                'ordering': ['reading_question', 'order'],
            },
        ),
        migrations.CreateModel(
            name='ReadingFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.FileField(upload_to=arcutils.path.UploadToPathAndRename('files/2017/10'))),
                ('type', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'reading_file',
            },
        ),
        migrations.CreateModel(
            name='ReadingMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reading', models.TextField()),
                ('difficulty', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'readings',
                'db_table': 'reading',
                'ordering': ['difficulty'],
            },
        ),
        migrations.CreateModel(
            name='ReadingQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('order', models.IntegerField(default=0)),
                ('reading_material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.ReadingMaterial')),
            ],
            options={
                'db_table': 'question',
                'ordering': ['reading_material', 'order'],
            },
        ),
        migrations.AddField(
            model_name='readingfile',
            name='reading_material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.ReadingMaterial'),
        ),
        migrations.AddField(
            model_name='questionchoice',
            name='reading_question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.ReadingQuestion'),
        ),
    ]
