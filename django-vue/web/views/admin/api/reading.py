from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from types import MethodType
import json
import pytz

from web.models.reading import *
from ...base import AdminView
from arcutils.time_helper import get_timestamp
from arcutils.reading_helper import *


def get_excerpt(input_str, max_len=50):
    if len(input_str) <= max_len:
        return input_str

    return input_str[:max_len - 3] + '...'

class AdminReadingApi(AdminView):
    NUM_PAGES = 30

    def get(self, request, **kwargs):
        response = {
            'status': 1,
            'err': 'Unknown command'
        }

        if 'page_action' in kwargs:
            page_action = kwargs['page_action']
            if page_action == 'add':
                self.set_page('reading', 'Add Reading')
                return self.render(request, 'arc/admin/reading-form.html')
            elif page_action == 'edit':
                self.set_page('reading', 'Edit Reading')
                return self.render(request, 'arc/admin/reading-form.html')
            elif page_action == 'delete':
                print('Delete.....')
                ReadingMaterial.objects.filter(pk=request.GET.get('id', -1)).delete()
                target_page = int(request.GET.get('page', 0))
                return redirect('/reading' + ('?page=' + str(target_page)) if target_page > 0 else '')
            elif page_action == 'list':
                readings = ReadingMaterial.objects.order_by('-created')
                reading_list = []

                paginator = Paginator(readings, self.NUM_PAGES)

                try:
                    shown_readings = paginator.page(request.GET.get('page', 1))
                except (ValueError, PageNotAnInteger, InvalidPage):
                    shown_readings = paginator.page(1)
                except EmptyPage:
                    shown_readings = paginator.page(paginator.num_pages)

                for reading in shown_readings.object_list:
                    questions = ReadingQuestion.objects.filter(reading_material=reading).all()
                    reading_list.append({
                        'id': reading.id,
                        'reading': reading.reading,
                        'excerpt': get_excerpt(reading.reading, 30),
                        'difficulty': "{:.1f}".format(decode_difficulty(reading.difficulty)),
                        'updated': get_timestamp(reading.updated),
                        'created': get_timestamp(reading.created),
                        'questions': len(questions)
                    })

                pagination_data = {
                    'start_index': shown_readings.start_index(),
                    'end_index': shown_readings.end_index(),
                    'has_next': shown_readings.has_next(),
                    'has_other_pages': shown_readings.has_other_pages(),
                    'has_previous': shown_readings.has_previous(),
                    'number': shown_readings.number,
                    'per_page': paginator.per_page,
                    'total_page': paginator.num_pages,
                    'total_items': paginator.count
                }
                self.context.update({'pagination': pagination_data})

                response = {
                    'status': 0,
                    'data': {
                        'reading': reading_list,
                        'pagination': pagination_data
                    }
                }

        return JsonResponse(response)

    def post(self, request, **kwargs):
        if 'page_action' in kwargs:
            if kwargs['page_action'] == 'add':
                retval = self.insert_new_reading(request)
                if retval['status'] == 0:
                    return JsonResponse(retval)
                else:
                    return JsonResponse({
                        'status': retval['status'] + retval.get('error_code', 0),
                        'err': 'Invalid data'})
            elif kwargs['page_action'] == 'edit':
                reading_id = request.GET.get('id', 0)
                request_type = 'request'
                if 'params' in request.POST:
                    params_data = json.loads(request.POST['params'])
                    request_type = params_data.get('type', 'request')

                if request_type == 'request':
                    retval = self.retrieve_reading(request, reading_id)
                    if retval['status'] == 0:
                        return JsonResponse(retval)
                    else:
                        return JsonResponse({
                            'status': retval['status'] + retval.get('error_code', 0),
                            'err': 'No valid data'})
                elif request_type == 'save':
                    retval = self.update_reading(request, reading_id)
                    if retval['status'] == 0:
                        return JsonResponse(retval)
                    else:
                        return JsonResponse({
                            'status': retval['status'] + retval.get('error_code', 0),
                            'err': 'No valid data'})

        print(kwargs['page_action'])
        return JsonResponse({'status': 1, 'err': 'Invalid action'})

    def retrieve_reading(self, request, reading_id):
        try:
            reading = ReadingMaterial.objects.get(pk=reading_id)
        except ReadingMaterial.DoesNotExist:
            return {'status': 1, 'error_code': 0}

        questions = ReadingQuestion.objects.filter(reading_material=reading).order_by('order').all()

        question_data = []
        for question in questions:
            choices = QuestionChoice.objects.filter(reading_question=question).order_by('order').all()
            choice_data = []
            answers = []
            for choice_index, choice in enumerate(choices):
                choice_data.append({'value': choice.choice_text})
                if choice.is_correct:
                    answers.append(choice_index)

            question_data.append({
                'question': question.question_text,
                'choices': choice_data,
                'answer': answers[0] if len(answers) > 0 else -1
            });

        reading_files = {}
        image_files = ReadingFile.objects.filter(reading_material=reading, type='image').all()
        if len(image_files) > 0:
            reading_files.update({'image': '/' + image_files[0].path.url})

        audio_files = ReadingFile.objects.filter(reading_material=reading, type='audio').all()
        if len(audio_files) > 0:
            reading_files.update({'audio': '/' + audio_files[0].path.url})

        reading_tags = reading.tags.all()
        reading_tags_str = ', '.join([tag.name for tag in reading_tags])

        return {
            'status': 0,
            'data': {
                'id': reading.id,
                'updated': get_timestamp(reading.updated),
                'status': reading.status,
                'reading': reading.reading,
                'difficulty': decode_difficulty(reading.difficulty),
                'questions': question_data,
                'files': reading_files,
                'tags': reading_tags_str
            }
        }

    def insert_new_reading(self, request):
        request_data = request.POST.get('data', None)
        if request_data is None:
            return {'status': 1, 'err_code': 0}

        print(request.POST['data'])
        reading_data = json.loads(request_data)

        if not all(k in reading_data for k in ('reading', 'difficulty')):
            return {'status': 1, 'err_code': 0}

        if len(reading_data['reading']) == 0:
            return {'status': 1, 'err_code': 0}

        print('### DATA OK   ###')
        print('### SAVING... ###')

        new_reading = ReadingMaterial()
        new_reading.reading = reading_data['reading']
        new_reading.difficulty = encode_difficulty(reading_data['difficulty'])
        new_reading.status = 0
        new_reading.save()

        # Handle the tags
        raw_tags = reading_data.get('tags', '').lower().split(",")
        request_tags = [tag.strip() for tag in raw_tags if len(tag) > 0]
        tags_object = Tag.objects.filter(name__in=request_tags).all()
        avail_tag = {tag.name: tag for tag in tags_object}

        for tag in request_tags:
            if tag in avail_tag:
                new_reading.tags.add(avail_tag[tag])
            else:
                new_tag = Tag()
                new_tag.name = tag
                new_tag.save()
                new_reading.tags.add(new_tag)

        request_question = reading_data.get('questions', [])

        for q_index, q_data in enumerate(request_question):
            question_data = ReadingQuestion()
            question_data.reading_material = new_reading

            question_data.question_text = q_data.get('question', '')
            question_data.order = q_index
            question_data.save()

            correct_answer = q_data.get('answer', -1)
            request_choices = q_data.get('choices', [])
            for c_index, c_data in enumerate(request_choices):
                choice_data = QuestionChoice()
                choice_data.reading_question = question_data
                choice_data.choice_text = c_data.get('value', '')
                choice_data.order = c_index
                choice_data.is_correct = True if c_index == correct_answer else False
                choice_data.save()

        reading_files = {}
        if 'image' in request.FILES:
            image_file = ReadingFile()
            image_file.reading_material = new_reading
            image_file.path = request.FILES['image']
            image_file.type = 'image'
            image_file.save()

            reading_files.update({'image': '/' + image_file.path.url})

        if 'audio' in request.FILES:
            audio_file = ReadingFile()
            audio_file.reading_material = new_reading
            audio_file.path = request.FILES['audio']
            audio_file.type = 'audio'
            audio_file.save()
            reading_files.update({'audio': '/' + audio_file.path.url})

        return {
            'status': 0,
            'data': {
                'id': new_reading.id,
                'updated': get_timestamp(new_reading.updated),
                'status': new_reading.status,
                'files': reading_files
            }
        }

    def update_reading(self, request, reading_id):
        # Check data in DB
        try:
            reading = ReadingMaterial.objects.get(pk=reading_id)
        except ReadingMaterial.DoesNotExist:
            return {'status': 1, 'error_code': 0}

        # Check request data
        request_data = request.POST.get('data', None)
        if request is None:
            return {'status': 1, 'err_code': 1}

        print(request.POST['data'])
        reading_data = json.loads(request_data)

        if not all(k in reading_data for k in ('reading', 'difficulty')):
            return {'status': 1, 'err_code': 1}

        if len(reading_data['reading']) == 0:
            return {'status': 1, 'err_code': 1}

        print('### DATA OK      ###')
        print('### UPDATIING... ###')

        reading.reading = reading_data['reading']
        reading.difficulty = encode_difficulty(reading_data['difficulty'])
        reading.status = reading_data.get('status', 0)
        reading.save()

        # Update Tags
        reading.tags.clear()
        raw_tags = reading_data.get('tags', '').lower().split(",")
        request_tags = [tag.strip() for tag in raw_tags if len(tag) > 0]
        tags_object = Tag.objects.filter(name__in=request_tags).all()
        avail_tag = {tag.name: tag for tag in tags_object}

        for tag in request_tags:
            if tag in avail_tag:
                reading.tags.add(avail_tag[tag])
            else:
                new_tag = Tag()
                new_tag.name = tag
                new_tag.save()
                reading.tags.add(new_tag)

        # Update question
        ReadingQuestion.objects.filter(reading_material=reading).delete()
        request_question = reading_data.get('questions', [])

        for q_index, q_data in enumerate(request_question):
            question_data = ReadingQuestion()
            question_data.reading_material = reading

            question_data.question_text = q_data.get('question', '')
            question_data.order = q_index
            question_data.save()

            correct_answer = q_data.get('answer', -1)
            request_choices = q_data.get('choices', [])
            for c_index, c_data in enumerate(request_choices):
                choice_data = QuestionChoice()
                choice_data.reading_question = question_data
                choice_data.choice_text = c_data.get('value', '')
                choice_data.order = c_index
                choice_data.is_correct = True if c_index == correct_answer else False
                choice_data.save()

        # Update files
        reading_files = {}
        if 'image' in request.FILES:
            ReadingFile.objects.filter(reading_material=reading, type='image').delete()
            image_file = ReadingFile()
            image_file.reading_material = reading
            image_file.path = request.FILES['image']
            image_file.type = 'image'
            image_file.save()
            reading_files.update({'image': '/' + image_file.path.url})

        if 'audio' in request.FILES:
            ReadingFile.objects.filter(reading_material=reading, type='audio').delete()
            audio_file = ReadingFile()
            audio_file.reading_material = reading
            audio_file.path = request.FILES['audio']
            audio_file.type = 'audio'
            audio_file.save()
            reading_files.update({'audio': '/' + audio_file.path.url})

        return {
            'status': 0,
            'data': {
                'id': reading.id,
                'updated': get_timestamp(reading.updated),
                'status': reading.status,
                'files': reading_files
            }
        }
