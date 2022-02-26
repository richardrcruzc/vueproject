from django.contrib.auth.models import User
from django.db import models
from .reading import ReadingMaterial, ReadingQuestion, QuestionChoice


class Classroom(models.Model):
    class Meta:
        db_table = 'classroom'

    name = models.CharField(max_length=255, default='', unique=True)
    level = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % self.name
