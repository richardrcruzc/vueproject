from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from ..base import ProtectedView

from django.shortcuts import redirect
from ...models.student import StudentScore, StudentProfile, StudentReport

from ..base import StudentView


class StudentGeneralReportView(StudentView):
    def get(self, request):
        student_scores = StudentScore.objects.filter(student=request.user).all().order_by('-created')[:10]
        profile = StudentProfile.objects.filter(student=request.user).first()

        base_score = profile.classroom.level
        # get 3 stars and trophy -----total_testing----------change--------------ftf----------------
        total_testing = 0
        if profile:
            total_test = StudentReport.objects.filter(student=request.user).count()
            total_testing = total_test
            if total_test > 3:
                if profile.rank <= base_score:
                    rank_badge = 1
                else:
                    class_students = profile.classroom.students.order_by('-rank').all()
                    total_student = len(class_students)
                    rank_badge = 2
                    if total_student > 0:
                        student_rank = 0
                        for student in class_students:
                            if student.student.id == profile.student.id:
                                break
                            student_rank = student_rank + 1

                        if student_rank < 0.3 * total_student:
                            rank_badge = 3
            else:
                rank_badge = 0
        else:
            total_testing = 0
            rank_badge = 0

        scores = [student_score.score - base_score for student_score in student_scores]
        if len(scores) > 0:
            lo_boundary = (min(scores) - 75)
            hi_boundary = max(scores) + 75
        else:
            lo_boundary = 0
            hi_boundary = 0

        retval = {
            'status': 0,
            'data': {
                'low': lo_boundary,
                'high': hi_boundary,
                'scores': list(reversed(scores)),
                'rank': rank_badge,
                'total_test': total_testing,
        }}
        return JsonResponse(retval)
