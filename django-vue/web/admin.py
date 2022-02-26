from django.contrib import admin
from .models.classroom import *
from .models.reading import *
from .models.student import *
from .models.teacher import *

# Register your models here.

admin.site.register(Classroom)
admin.site.register(Tag)
admin.site.register(ReadingMaterial)
admin.site.register(ReadingFile)
admin.site.register(ReadingQuestion)
admin.site.register(QuestionChoice)
admin.site.register(StudentProfile)
admin.site.register(StudentReport)
admin.site.register(StudentScore)
admin.site.register(ReportDetail)
admin.site.register(TeacherProfile)