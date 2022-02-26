from django.contrib.auth.models import User
from django.db import models
from .classroom import Classroom


class TeacherProfile(models.Model):
    class Meta:
        db_table = 'teacher_profile'

    fullname = models.CharField(max_length=255, default='')
    teacher = models.OneToOneField(User, primary_key=True, related_name='teacher_profile')
    classrooms = models.ManyToManyField(Classroom, blank=True)
    change_password = models.BooleanField(default=True)

    def __str__(self):
        return "%s - %s" % (self.teacher.id, self.fullname)