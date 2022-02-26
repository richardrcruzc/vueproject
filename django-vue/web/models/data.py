from django.db import models

class grade_info(models.Model):
    class Meta:
        db_table = 'grade_info'

    grade = models.IntegerField()
    text = models.CharField(max_length=50)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.text