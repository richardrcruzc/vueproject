# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-04-09 15:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0004_auto_20180401_2305'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'classroom',
            },
        ),
        migrations.CreateModel(
            name='StudentScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'student_score',
            },
        ),
        migrations.CreateModel(
            name='TeacherProfile',
            fields=[
                ('fullname', models.CharField(default='', max_length=255)),
                ('teacher', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='teacher_profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('classrooms', models.ManyToManyField(blank=True, to='web.Classroom')),
            ],
            options={
                'db_table': 'teacher_profile',
            },
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='teacher',
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='fullname',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='studentscore',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='classroom',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Classroom'),
        ),
    ]
