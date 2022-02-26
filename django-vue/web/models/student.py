from django.contrib.auth.models import User
from django.db import models
from .reading import ReadingMaterial, ReadingQuestion, QuestionChoice
from .classroom import Classroom


class StudentProfile(models.Model):
    class Meta:
        db_table = 'student_profile'

    fullname = models.CharField(max_length=255, default='')
    student = models.OneToOneField(User, primary_key=True, related_name = 'profile')
    is_new = models.BooleanField(default=True)
    change_password = models.BooleanField(default=True)
    avatar = models.SmallIntegerField(null=True)
    rank = models.IntegerField(default=0)
    #teacher = models.ForeignKey(User, default=1, related_name = 'has_students')
    classroom = models.ForeignKey(Classroom, null=True, related_name='students')

    def __str__(self):
        return "%s" % self.student


class StudentReport(models.Model):
    class Meta:
        db_table = 'student_report'

    student = models.ForeignKey(User)
    reading = models.ForeignKey(ReadingMaterial)
    taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s, %s" % (self.student.id, self.reading.id)


class StudentScore(models.Model):
    class Meta:
        db_table = 'student_score'

    student = models.ForeignKey(User)
    score = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s, %s" % (self.student.id, self.score)


class ReportDetail(models.Model):
    class Meta:
        db_table = 'report_detail'

    student_report = models.ForeignKey(StudentReport)
    question = models.ForeignKey(ReadingQuestion)
    choice = models.ForeignKey(QuestionChoice)
    is_correct = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.student_report
