from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from types import MethodType
import json

from ..base import StudentView
from ...models.reading import *
from ...models.student import *
from arcutils.time_helper import get_timestamp

from django.contrib.auth.models import User, Group
from django.db.models.aggregates import Count
from django.db import IntegrityError
from random import randint


class QuizView(StudentView):
    def get(self, request, **kwargs):
        self.set_page('test', 'Quiz')
        if 'page_action' in kwargs:
            if kwargs['page_action'] == 'start':
                self.set_page('test', 'Quiz')
                return self.render(request, 'arc/student/quiz.html')
            elif kwargs['page_action'] == 'Quiz':
                self.set_page('test', 'mm')
                return self.render(request, 'arc/student/quiz-mm.html')
        else:
            pass
        return redirect('dashboard')

    def post(self, request, **kwargs):
        if 'page_action' in kwargs:
            if kwargs['page_action'] == 'question':
                retval = self.get_quiz_data(request)
                if retval['status'] == 0:
                    return JsonResponse(retval)
                else:
                    return JsonResponse({
                        'status': retval['status'] + retval.get('error_code', 0),
                        'err': 'Invalid data'})
            elif kwargs['page_action'] == 'mm':
                retval = self.get_quiz_data_mm(request)
                if retval['status'] == 0:
                    return JsonResponse(retval)
                else:
                    return JsonResponse({
                        'status': retval['status'] + retval.get('error_code', 0),
                        'err': 'Invalid data'})
            elif kwargs['page_action'] == 'answer':
                retval = self.check_answer(request);
                if retval['status'] == 0:
                    return JsonResponse(retval)
                else:
                    return JsonResponse({
                        'status': retval['status'] + retval.get('error_code', 0),
                        'err': 'Invalid data'})
            elif kwargs['page_action'] == 'learning':
                return JsonResponse({'status': 0})

        return JsonResponse({'status': 1, 'err': 'Invalid action'})

    def get_quiz_data(self, request):
        current_student = request.user
        rank = 0
        if current_student.profile:
            rank = current_student.profile.rank

        #print("rank: " + str(rank))
        DIFF_RANGE = 300
        try:
            user_reports = current_student.studentreport_set.values_list('reading', flat=True).all()

            # TODO: Run Adaptive algo right here to get relevant questions
            # Currently just randomize the question
            query_exclude = {
                'id__in': user_reports
            }

            query_filters = {
                'status': 10,
                'difficulty__lte': rank + DIFF_RANGE,
                'difficulty__gte': rank - DIFF_RANGE
            }

            print(user_reports)
            total_reading = ReadingMaterial.objects.exclude(**query_exclude).filter(**query_filters).aggregate(count=(Count('id')))['count']
            # Make sure can return something
            if total_reading == 0:
                query_exclude = {}
                total_reading = ReadingMaterial.objects.exclude(**query_exclude).filter(**query_filters).aggregate(count=(Count('id')))[
                    'count']

                if total_reading == 0:
                    query_filters = {'status': 10}
                    total_reading = ReadingMaterial.objects.exclude(**query_exclude).filter(**query_filters).aggregate(
                        count=(Count('id')))[
                        'count']

            print(total_reading)
            random_index = randint(0, total_reading-1)
            reading = ReadingMaterial.objects.exclude(**query_exclude).filter(**query_filters).all()[random_index]

        except Exception as ex:
            print(ex)
            return {'status': 1, 'error_code': 0}

        questions = ReadingQuestion.objects.filter(reading_material=reading).order_by('order').all()
        # import pdb;pdb.set_trace()
        # questions = []
        # questions.append(ReadingQuestion.objects.order_by('-id')[0])

        question_data = []
        for question in questions:
            choices = QuestionChoice.objects.filter(reading_question=question).order_by('order').all()
            choice_data = []
            answers = []
            if question.tutorial_file:
                tutorial = '/'+question.tutorial_file.url
            else:
                tutorial = None
            for choice_index, choice in enumerate(choices):
                choice_data.append({'value': choice.choice_text})
                if choice.is_correct:
                    answers.append(choice_index)

            if len(answers) > 0:
                question_data.append({
                    'id': question.pk,
                    'question': question.question_text,
                    'choices': choice_data,
                    'tutorial_file': tutorial,
                })

        reading_files = {}
        image_files = ReadingFile.objects.filter(reading_material=reading, type='image').all()
        if len(image_files) > 0:
            reading_files.update({'image': '/' + image_files[0].path.url})

        audio_files = ReadingFile.objects.filter(reading_material=reading, type='audio').all()
        if len(audio_files) > 0:
            reading_files.update({'audio': '/' + audio_files[0].path.url})

        student_profile = StudentProfile.objects.filter(student=current_student).first()
        if student_profile:
            student_profile.is_new = False
            student_profile.save()

        """
        quiz_report = StudentReport()
        quiz_report.student = current_student
        quiz_report.reading = reading
        quiz_report.save()
        """

        return {
            'status': 0,
            'data': {
                'id': reading.id,
                'status': reading.status,
                'reading': reading.reading,
                'questions': question_data,
                'level': int(reading.difficulty/1000),
                #'qtoken': quiz_report.id,
                'files': reading_files,
            }
        }

    def get_quiz_data_mm(self, request):
        try:
            reading = ReadingMaterial.objects.get(id=1)
        except:
            return {'status': 1, 'error_code': 0}

        questions = ReadingQuestion.objects.filter(reading_material=reading).order_by('order').all()

        question_data = []
        for question in questions:
            choices = QuestionChoice.objects.filter(reading_question=question).order_by('order').all()
            choice_data = []
            answers = []
            if question.tutorial_file:
                tutorial = '/'+question.tutorial_file.url
            else:
                tutorial = None
            for choice_index, choice in enumerate(choices):
                choice_data.append({'value': choice.choice_text})
                if choice.is_correct:
                    answers.append(choice_index)

            if len(answers) > 0:
                question_data.append({
                    'id': question.pk,
                    'question': question.question_text,
                    'choices': choice_data,
                    'tutorial_file': tutorial,
                })

        reading_files = {}
        image_files = ReadingFile.objects.filter(reading_material=reading, type='image').all()
        if len(image_files) > 0:
            reading_files.update({'image': '/' + image_files[0].path.url})

        audio_files = ReadingFile.objects.filter(reading_material=reading, type='audio').all()
        if len(audio_files) > 0:
            reading_files.update({'audio': '/' + audio_files[0].path.url})

        return {
            'status': 0,
            'data': {
                'id': reading.id,
                'status': reading.status,
                'reading': reading.reading,
                'questions': question_data,
                'files': reading_files,
            }
        }

    def check_answer(self, request):
        request_data = request.POST.get('data', None)
        if request_data is None:
            return {'status': 1, 'err_code': 0}

        question_data = json.loads(request_data)

        if not all(k in question_data for k in ('answer', 'question', 'token')):
            return {'status': 1, 'err_code': 0}

        try:
            question = ReadingQuestion.objects.get(pk=question_data['question'])
        except ReadingQuestion.DoesNotExist:
            return {'status': 1, 'error_code': 0}

        is_new_quiz = False
        try:
            token = question_data['token']
            if token > 0:
                quiz_report = StudentReport.objects.filter(id=token).first()
            else:
                is_new_quiz = True

                # Create new report
                quiz_report = StudentReport()
                quiz_report.student = request.user
                quiz_report.reading = question.reading_material
                quiz_report.save()
        except Exception as ex:
            return {'status': 1, 'error_code': 2}

        user_answer = int(question_data['answer'])
        choices = QuestionChoice.objects.filter(reading_question=question).order_by('order').all()
        if user_answer >= len(choices):
            return {'status': 1, 'error_code': 1}

        report_detail = ReportDetail()
        report_detail.student_report = quiz_report
        report_detail.question = question
        report_detail.choice = choices[user_answer]
        report_detail.is_correct = choices[user_answer].is_correct
        report_detail.save()

        # TODO: Fix scoring system here
        student_profile = request.user.profile
        #print('student profile %s' % student_profile.rank)
        #print(question.reading_material.difficulty)
        BASE_SCORE = 300
        TOTAL_OPTIONS = 4
        difficulty_factor = abs((question.reading_material.difficulty - student_profile.rank + BASE_SCORE) / TOTAL_OPTIONS)

        reverse_difficulty_factor = (BASE_SCORE * 2 / TOTAL_OPTIONS) - difficulty_factor
        # print(difficulty_factor)

        rank_modifier = difficulty_factor / 8
        reverse_rank_modifier = reverse_difficulty_factor / 8

        # print(difficulty_factor)
        # rank = rank - difficulty_factor

        if choices[user_answer].is_correct:
            #answer_trials = ReportDetail.objects.filter(student_report=quiz_report).count()
            student_profile.rank = student_profile.rank + int(rank_modifier)
        else:
            student_profile.rank = student_profile.rank - int(reverse_rank_modifier)
        student_profile.save()

        if is_new_quiz:
            student_score = StudentScore()
            student_score.score = student_profile.rank
            student_score.student = request.user
            student_score.save()
        else:
            student_score = StudentScore.objects.filter(student=request.user).order_by('-created').first()
            student_score.score = student_profile.rank
            student_score.save()

        if choices[user_answer].is_correct:
            return {'status': 0, 'correct': 1, 'qtoken': quiz_report.id}
        else:
            return {'status': 0, 'correct': 0, 'qtoken': quiz_report.id}
