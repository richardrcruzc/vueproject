from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from ..base import ProtectedView
from ...models import ReadingMaterial
from ...models.teacher import TeacherProfile

from django.contrib.auth.models import User, Group

class AdminView(ProtectedView):
    def get(self, request):
        teacher_profile = TeacherProfile.objects.filter(teacher=request.user).first()

        if teacher_profile is None:
            teacher_profile = TeacherProfile()
            teacher_profile.teacher = request.user
            teacher_profile.save()

        if teacher_profile.change_password:
            # Force change password
            return HttpResponseRedirect('/update-password/')

        self.set_page('dashboard')
        reading_total = ReadingMaterial.objects.count()

        total_student = 0
        student_reports = []
        is_admin = False
        try:
            if request.user.groups.filter(name__in=['admin']).exists():
                is_admin = True
                total_student = User.objects.filter(groups__name='student').count()
            else:
                # is_admin = False
                for avail_class in teacher_profile.classrooms.all():
                    base_score = avail_class.level
                    class_students = avail_class.students.order_by('-rank').all()

                    student_report = [0, 0, 0, 0]
                    for student_profile in class_students:
                        total_test = StudentReport.objects.filter(student=student_profile.student).count()
                        if total_test > 3:
                            if student_profile.rank >= base_score + 500:
                                student_report[0] = student_report[0] + 1
                            elif student_profile.rank <= base_score - 100:
                                student_report[2] = student_report[2] + 1
                            else:
                                student_report[1] = student_report[1] + 1
                        else:
                            student_report[3] = student_report[3] + 1

                    student_reports.append({'class': avail_class.name, 'report': student_report, 'total': len(class_students)})

                total_student = StudentProfile.objects.filter(classroom__in=teacher_profile.classrooms.all()).count()
        except Exception as ex:
            print('Error in getting student report:', ex)


        self.context.update({
            'user_data': {
                'student': total_student,
                'reports': student_reports,
            },
            'readings_data': {
                'total': ReadingMaterial.objects.count(),
                'draft': ReadingMaterial.objects.filter(status=0).count(),
                'published': ReadingMaterial.objects.filter(status=10).count()
            }
        })
        # print(self.context['readings_data'])
        self.context.update({'is_admin': is_admin})
        return self.render(request, 'arc/admin/dashboard.html')


from ...models.student import *
from ...models.classroom import *
from django.conf import settings
from django.http import JsonResponse

"""
import pandas as pd
import os, math

class AccountSetupView(AdminView):
    def open_file(self, file_name):
        file_path = os.path.join(settings.STATICFILES_DIRS[0], 'accounts', file_name)
        print(file_path)
        user_data = []
        try:
            xl_file = pd.ExcelFile(file_path)

            for sheet in xl_file.sheet_names:
                df = xl_file.parse(sheet)

                students = [df['Student Name'], df['User Account']]
                student_data = []
                for i in range(0, len(students[0])):
                    student_data.append({
                        'name': students[0][i],
                        'username': students[1][i]
                    })

                teachers = [df['Teacher Name'], df['Teacher Account']]
                teacher_data = []
                for i in range(0, len(teachers[0])):
                    if pd.isnull(teachers[0][i]):
                        break

                    teacher_data.append({
                        'name': teachers[0][i],
                        'username': teachers[1][i]
                    })

                class_details = df['School Details']
                level = 0
                if len(class_details[1]) == 2:
                    if class_details[1][0].lower() == 'p':
                        level = int(class_details[1][1])
                    elif class_details[1][0].lower() == 's':
                        level = 6 + int(class_details[1][1])

                user_data.append({
                    'class': class_details[0],
                    'level': level * 1000,
                    'teachers': teacher_data,
                    'students': student_data
                })

        except Exception as ex:
            print('Exception:', ex)

        return user_data

    def get(self, request, **kwargs):
        class_data = self.open_file('test.xlsx')
        print(class_data)

        # create classroom
        for current_class in class_data:
            class_rank = current_class['level']
            try:
                classroom = Classroom.objects.get(name=current_class['class'])
            except ObjectDoesNotExist:
                classroom = Classroom()
                classroom.name = current_class['class']

            classroom.level = class_rank
            classroom.save()

            # Create Teacher Accounts
            try:
                teacher_group = Group.objects.get(name='teacher')
            except ObjectDoesNotExist:
                teacher_group = Group()
                teacher_group.name = 'teacher'
                teacher_group.save()

            for class_teacher in current_class['teachers']:
                teacher_username = class_teacher['username'].strip().lower()
                try:
                    teacher = User.objects.get(username=teacher_username)
                except ObjectDoesNotExist:
                    teacher = User()
                    teacher.username = teacher_username
                    teacher.set_password(teacher_username)
                    teacher.save()

                teacher.groups.add(teacher_group)
                teacher.save()

                # Create Teacher Profile
                try:
                    teacher_profile = TeacherProfile.objects.get(teacher=teacher)
                except ObjectDoesNotExist:
                    teacher_profile = TeacherProfile()
                    teacher_profile.teacher = teacher
                    teacher_profile.fullname = class_teacher['name']
                    teacher_profile.save()

                teacher_profile.classrooms.add(classroom)
                teacher_profile.save()

            # Create Student Accounts
            try:
                student_group = Group.objects.get(name='student')
            except ObjectDoesNotExist:
                student_group = Group()
                student_group.name = 'student'
                student_group.save()

            for student in current_class['students']:
                # create user
                student_username = student['username'].strip().lower()
                try:
                    new_student = User.objects.get(username=student_username)
                except ObjectDoesNotExist:
                    new_student = User()
                    new_student.username = student_username
                    new_student.set_password(student_username)
                    new_student.save()

                    new_student.groups.add(student_group)
                    new_student.save()

                try:
                    student_profile = StudentProfile.objects.get(student=new_student)
                except ObjectDoesNotExist:

                    student_profile = StudentProfile()
                    student_profile.student = new_student
                    student_profile.fullname = student['name']
                    student_profile.classroom = classroom
                    student_profile.save()

                if student_profile.classroom == classroom:
                    student_profile.rank = class_rank
                    student_profile.save()
                else:
                    print('Inconsistent user data:', student_username)

        return JsonResponse({'data': class_data})

"""