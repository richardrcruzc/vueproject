from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from arcutils.path import *
import os
import time


class Tag(models.Model):
    class Meta:
        db_table = 'tag'

    name = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.name


class ReadingMaterial(models.Model):
    class Meta:
        db_table = 'reading'
        verbose_name_plural = 'readings'
        ordering = ['difficulty']

    title = models.CharField(max_length=255, default="")
    reading = models.TextField(null=False, blank=False)
    difficulty = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, default=1)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return "%s" % self.reading


class ReadingFile(models.Model):
    class Meta:
        db_table = 'reading_file'

    reading_material = models.ForeignKey(ReadingMaterial, on_delete=models.CASCADE)
    path = models.FileField(
        upload_to=UploadToPathAndRename(time.strftime("files" + os.path.sep + "%Y" + os.path.sep + "%m")))
    type = models.CharField(max_length=50)

class ReadingQuestion(models.Model):
    class Meta:
        db_table = 'question'
        ordering = ['reading_material', 'order']

    reading_material = models.ForeignKey(ReadingMaterial, on_delete=models.CASCADE)
    tutorial_file = models.FileField(
        upload_to=UploadToPathAndRename(time.strftime("files/tutorial" + os.path.sep + "%Y" + os.path.sep + "%m")), null=True, blank=True)
    question_text = models.CharField(max_length=200)
    order = models.IntegerField(default=0)

    def __str__(self):
        return "%s" % self.question_text


class QuestionChoice(models.Model):
    class Meta:
        db_table = 'question_choice'
        ordering = ['reading_question', 'order']

    reading_question = models.ForeignKey(ReadingQuestion, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    def __str__(self):
        return "[%s] %s" % ('Correct' if self.is_correct else 'Wrong', 'answer')


@receiver(post_delete, sender=ReadingFile)
def reading_file_post_delete_handler(sender, **kwargs):
    local_file = kwargs['instance']
    storage, path = local_file.path.storage, local_file.path.path
    storage.delete(path)
