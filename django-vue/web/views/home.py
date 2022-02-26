from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .base import BaseView, ProtectedView
from .admin.home import AdminView
from .student.home import StudentView
from ..models.student import StudentProfile
from ..models.teacher import TeacherProfile


class HomeView(BaseView):
    def get(self, request):
        if request.user.is_authenticated:
            return DashboardView().get(request)
        else:
            return render(request, 'arc/index.html')


class PasswordView(BaseView):
    def get(self, request):
        self.context.update({'page_title': ' '})
        return self.render(request, 'arc/student/password.html')

    def post(self, request):
        self.context.update({'page_title': ' '})

        error_message = ''
        password = [request.POST.get('password', ''), request.POST.get('password_repeat', '')]
        if len(password[0]) + len(password[1]) == 0:
            error_message = 'Masukkan kata laluan baharu'
        elif password[0] != password[1]:
            error_message = 'Kata laluan tidak sama'
        elif request.user.username == password[0]:
            error_message = 'Kata laluan tidak boleh sama dengan ID Pengguna'

        if len(error_message) > 0:
            self.context.update({'error_message': error_message})
            return self.render(request, 'arc/student/password.html')
        else:
            # update password
            profile = None
            if request.user.groups.filter(name__in=['admin', 'teacher']).exists():
                profile = TeacherProfile.objects.filter(teacher=request.user).first()
            else:
                profile = StudentProfile.objects.filter(student=request.user).first()

            if profile:
                current_user = User.objects.filter(username=request.user.username).first()
                if current_user:
                    current_user.set_password(password[0])
                    current_user.save()

                profile.change_password = False
                profile.save()

            return HttpResponseRedirect('/dashboard/')


class VueView(BaseView):
    def get(self, request):
        return render(request, 'arc/index_test.html')


class DashboardView(BaseView):
    def get(self, request):
        if request.user.groups.filter(name__in=['admin', 'teacher']).exists():
            return AdminView.as_view()(request)
        else:
            return StudentView.as_view()(request)


from django.http import JsonResponse
from ..models.reading import *
from collections import Counter
from arcutils.reading_helper import *
import re
from django.utils.text import Truncator

class TestView(BaseView):
    def get(self, request):
        filter_regex = 's2'
        filter_status = [0, 10]
        readings = ReadingMaterial.objects.filter(tags__name__regex = r'' + filter_regex,
                                                  status__in=filter_status).order_by('id').all()

        data = []
        score_list = []
        adj_score = 0
        for reading in readings:

            words = re.findall(r'\w+', reading.reading.lower())
            word_list = Counter(words).most_common()
            difficulty_score = compute_reading_difficulty(reading.reading)
            #adj_score = (difficulty_score[0] * 1000) + (80 * difficulty_score[2])

            #adj_score = round((difficulty_score[0] - 0.5) / (9-0.5) * 10) * 100 + 8000

            score_list.append(difficulty_score[0])
            questions = ReadingQuestion.objects.filter(reading_material=reading).all()
            question_data = []
            for question in questions:
                choices = QuestionChoice.objects.filter(reading_question=question).all()
                choice_data = []
                for choice in choices:
                    choice_data.append({
                        'text': 'C_OK' if len(choice.choice_text) > 0 else '-'
                    })
                if len(choice_data) >= 4:
                    question_data.append({
                        'text': 'QOK' if len(question.question_text) > 0 else '-',
                        'choices': choice_data
                    })

            if len(question_data) >= 4:
                data.append({
                    'id': reading.id,
                    'reading': reading.reading[:30],
                    'questions': question_data,
                    'reading_full': reading.reading,
                    'difficulty': reading.difficulty,
                    'words': word_list,
                    'total_unique_word': len(word_list),
                    'total_word': difficulty_score[2],
                    'total_syllable': difficulty_score[3],
                    'total_sentence': difficulty_score[4],
                    'adj_score': "{0:.2f}".format(adj_score),
                    'score': "{0:.2f}".format(difficulty_score[0]),
                })
        """
        return JsonResponse({
            'status': 0,
            'data': data
        })
        """

        params = {
            'readings': data,
            'scores': sorted(score_list)
        }
        return render(request, 'arc/test2.html', params)
