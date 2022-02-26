from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from types import MethodType
import json
import pytz
import re
from collections import Counter

from web.models.reading import *
from ..base import AdminView
from arcutils.time_helper import get_timestamp
from arcutils.reading_helper import *

from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile


class AdminTestingView(AdminView):
    NUM_PAGES = 30

    def get(self, request, **kwargs):
        self.set_page('test', 'Senarai ujian')

        if 'page_action' in kwargs:
            if kwargs['page_action'] == 'add':
                self.set_page('test', 'Tambah Bacaan')
                return self.render(request, 'arc/admin/reading-form.html')
            elif kwargs['page_action'] == 'edit':
                self.set_page('reading', 'Edit Bacaan')
                return self.render(request, 'arc/admin/test-form.html')
            elif kwargs['page_action'] == 'delete':
                print('Delete.....')

                try:
                    if request.user.groups.filter(name__in=['admin']).exists():
                        ReadingMaterial.objects.filter(pk=request.GET.get('id', -1)).delete()
                    else:
                        ReadingMaterial.objects.filter(author=request.user, pk=request.GET.get('id', -1)).delete()
                except ReadingMaterial.DoesNotExist:
                    return JsonResponse({'status': 1, 'error_code': 0})

                target_page = int(request.GET.get('page', 0))
                return redirect('/test_list' + ('?page=' + str(target_page)) if target_page > 0 else '')
            elif kwargs['page_action'] == 'preview':
                self.set_page('reading', 'Bacaan')
                reading = ReadingMaterial.objects.filter(pk=request.GET.get('id', -1)).first()
                if not reading:
                    target_page = int(request.GET.get('page', 0))
                    return redirect('/test_list' + ('?page=' + str(target_page)) if target_page > 0 else '')

                questions = ReadingQuestion.objects.filter(reading_material=reading).all()

                question_data = []
                for question in questions:
                    choices = QuestionChoice.objects.filter(reading_question=question).order_by('order').all()
                    choices_data = []
                    for choice in choices:
                        choices_data.append({'text': choice.choice_text})

                    question_data.append({
                        'question': question.question_text,
                        'choices': choices_data
                    })

                reading_data = {
                    'id': reading.id,
                    'reading': reading.reading,
                    'title': reading.title,
                    'questions': question_data
                }

                image_files = ReadingFile.objects.filter(reading_material=reading, type='image').all()
                audio_files = ReadingFile.objects.filter(reading_material=reading, type='audio').all()
                if len(image_files) > 0:
                    reading_data['media_avail'] = True
                    reading_data['image'] = '/' + image_files[0].path.url

                if len(audio_files) > 0:
                    reading_data['media_avail'] = True
                    reading_data['audio'] = '/' + audio_files[0].path.url

                self.context.update({'reading': reading_data})
                return self.render(request, 'arc/admin/quiz.html')
            elif kwargs['page_action'] == 'test':
                return JsonResponse({'status': '111'})
            else:
                return redirect('/test_list/')
        else:
            readings = None
            is_admin = False

            template_filter = ''
            try:
                filter = request.GET.get('filter', 0)
            except:
                print('filter error')

            filter_regex = ''
            try:
                req_levels = []
                req_levels_str = request.GET.getlist('level', [])

                for level in req_levels_str:
                    current_level = int(level)
                    req_levels.append(current_level)
                    template_filter = template_filter + '&level=' + str(current_level)
                    if 1 <= current_level and current_level <= 6:
                        filter_regex = filter_regex + '|p' + str(current_level)
                    elif 7 <= current_level and current_level <= 10:
                        filter_regex = filter_regex + '|s' + str(current_level - 6)

                req_published = int(request.GET.get('published', 0))
                req_review = int(request.GET.get('review', 0))
                req_draft = int(request.GET.get('draft', 0))

                if (len(req_levels) == 0 and (req_published + req_review + req_draft) == 0) or \
                        (len(req_levels) == 10 and (req_published + req_review + req_draft) == 3):
                    new_filter = 0
                else:
                    new_filter = 1

                    filter_status = []
                    if req_published:
                        template_filter = template_filter + '&published=1'
                        filter_status.append(10)
                    if req_review:
                        template_filter = template_filter + '&review=1'
                        filter_status.append(5)
                    if req_draft:
                        template_filter = template_filter + '&draft=1'
                        filter_status.append(0)
            except Exception as ex:
                new_filter = 0

            if new_filter == 0:
                template_filter = ''

            if request.user.groups.filter(name__in=['admin']).exists():
                if new_filter == 0:
                    testings = ReadingQuestion.objects.order_by('-id')
                else:
                    testings = ReadingQuestion.objects.filter(tags__name__regex=r'' + filter_regex[1:],
                                                              status__in=filter_status).order_by('-updated')

                """
                if filter == 0:
                    readings = ReadingMaterial.objects.order_by('-updated')
                else:
                    #filter_tags = Tag.objects.filter(name__contains='p3').all()
                    #filter_tags = Tag.objects.filter(name__regex = r'(p3|p4|p5)').readingmaterial_set.all()
                    #for filter in filter_tags:
                    #    print(filter)
                    #tags__name__regex=r'p3|p4|p5'
                    readings = ReadingMaterial.objects.filter(tags__name__regex=r'p3|p4|p5').order_by('-updated')
                """

                is_admin = True
            # else:
            #     if new_filter == 0:
            #         readings = ReadingQuestion.objects.filter(author=request.user).order_by('-updated')
            #     else:
            #         readings = ReadingMaterial.objects.filter(author=request.user,
            #                                                   tags__name__regex=r'' + filter_regex[1:],
            #                                                   status__in=filter_status).order_by('-updated')
            #     """
            #     if filter == 0:
            #         readings = ReadingMaterial.objects.filter(author=request.user).order_by('-updated')
            #     else:
            #         readings = ReadingMaterial.objects.filter(author=request.user, tags__name__regex=r'p3|p4|p5').order_by('-updated')
            #     """

            testing_list = []

            paginator = Paginator(testings, self.NUM_PAGES)

            try:
                shown_testings = paginator.page(request.GET.get('page', 1))
            except (ValueError, PageNotAnInteger):
                shown_testings = paginator.page(1)
            except (EmptyPage, InvalidPage):
                shown_testings = paginator.page(paginator.num_pages)

            for testing in shown_testings.object_list:
                # tag = testing.tags.first()
                reading = ReadingMaterial.objects.filter(id=testing.reading_material_id).first()
                answer = QuestionChoice.objects.filter(reading_question_id=testing.id, is_correct=True).first()
                if reading.status == 10:
                    testing_status = 'Terbit'
                elif reading.status == 5:
                    testing_status = 'Tinjauan'
                else:
                    testing_status = 'Draf'
                # questions = ReadingQuestion.objects.filter(reading_material=reading).all()
                r_video_upload = ReadingFile.objects.filter(reading_material=reading).all()
                # q_video_upload = ReadingQuestion.objects.filter(reading_material=reading).all()
                # question_video = len(q_video_upload)
                reading_video = len(r_video_upload)
                if testing.tutorial_file =='':
                    uploads = reading_video
                else:
                    uploads = reading_video+1
                testing_list.append({
                    'id': testing.id,
                    'r_id': reading.id,
                    'status': testing_status,
                    'problem': testing.question_text,
                    'title': reading.title,
                    # 'level': tag if tag else 'N/A',
                    'video_upload': uploads,
                    'difficulty': "{:.1f}".format(decode_difficulty(reading.difficulty)),
                    'updated': get_timestamp(reading.updated),
                    'author': reading.author.username,
                    'created': get_timestamp(reading.created),
                    # 'questions': len(questions)
                })

            self.context.update({'testing_data': testing_list})

            shown_pages = 2

            # check first page
            paginator_range_first = shown_testings.number - shown_pages
            if paginator_range_first < 3:
                # shown_pages = shown_pages + (1 - paginator_range_first)
                paginator_range_first = 1
                paginator_range_last = 2 * shown_pages + 1
            else:
                paginator_range_last = shown_testings.number + shown_pages

            """
            paginator_range_first = ((shown_readings.number-1) // MAX_SHOWN_PAGE) * MAX_SHOWN_PAGE
            paginator_range_last = paginator_range_first + MAX_SHOWN_PAGE
            """

            if paginator_range_last > paginator.num_pages:
                paginator_range_last = paginator.num_pages
            elif paginator_range_last == paginator.num_pages - 1:
                paginator_range_last = paginator.num_pages
                paginator_range_first = paginator_range_first + 1

            pagination_data = {
                'start_index': shown_testings.start_index(),
                'end_index': shown_testings.end_index(),
                'has_next': shown_testings.has_next(),
                'has_other_pages': shown_testings.has_other_pages(),
                'has_previous': shown_testings.has_previous(),
                'number': shown_testings.number,
                'per_page': paginator.per_page,
                'shown_pages': [paginator_range_first, paginator_range_last],
                'total_page': paginator.num_pages,
                'total_items': paginator.count,
            }
            self.context.update({'pagination': pagination_data})
            self.context.update({'is_admin': is_admin})
            if len(template_filter) > 0:
                self.context.update({'filter_template': template_filter[1:]})
            self.context.update({'filter': filter})

            return self.render(request, 'arc/admin/test.html')

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

                is_admin = False
                try:
                    if request.user.groups.filter(name__in=['admin']).exists():
                        reading = ReadingMaterial.objects.get(pk=reading_id)
                        is_admin = True
                    else:
                        reading = ReadingMaterial.objects.get(author=request.user, pk=reading_id)
                except ReadingMaterial.DoesNotExist:
                    return JsonResponse({'status': 1, 'error_code': 0})

                if request_type == 'request':
                    retval = self.retrieve_reading(request, reading)
                    if retval['status'] == 0:
                        return JsonResponse(retval)
                    else:
                        return JsonResponse({
                            'status': retval['status'] + retval.get('error_code', 0),
                            'err': 'No valid data'})
                elif request_type == 'save':
                    retval = self.update_reading(request, reading, is_admin)
                    if retval['status'] == 0:
                        return JsonResponse(retval)
                    else:
                        return JsonResponse({
                            'status': retval['status'] + retval.get('error_code', 0),
                            'err': 'No valid data'})
            elif kwargs['page_action'] == 'calculate':
                return JsonResponse(self.calculate_reading_content(request))

        return JsonResponse({'status': 1, 'err': 'Invalid action'})

    def retrieve_reading(self, request, reading):
        questions = ReadingQuestion.objects.filter(reading_material=reading).order_by('order').all()
        # import pdb;pdb.set_trace()
        question_data = []
        for question in questions:
            choices = QuestionChoice.objects.filter(reading_question=question).order_by('order').all()
            choice_data = []
            answers = []
            for choice_index, choice in enumerate(choices):
                choice_data.append({'value': choice.choice_text})
                if choice.is_correct:
                    answers.append(choice_index)
            try:
                tutorial = '/' + question.tutorial_file.url
            except:
                tutorial = ''
            # import pdb;pdb.set_trace()
            question_data.append({
                'question': question.question_text,
                'choices': choice_data,
                'answer': answers[0] if len(answers) > 0 else -1,
                'tutorial': tutorial
            })

        reading_files = {}
        image_files = ReadingFile.objects.filter(reading_material=reading, type='image').all()
        if len(image_files) > 0:
            reading_files.update({'image': '/' + image_files[0].path.url})

        audio_files = ReadingFile.objects.filter(reading_material=reading, type='audio').all()
        if len(audio_files) > 0:
            reading_files.update({'audio': '/' + audio_files[0].path.url})

        reading_tags = reading.tags.all()
        reading_tags_str = ', '.join([tag.name for tag in reading_tags])

        words = re.findall(r'\w+', reading.reading.lower())
        word_list = Counter(words).most_common()

        difficulty_score = compute_reading_difficulty(reading.reading)

        lexical_diversity = 0
        if len(words) > 0:
            lexical_diversity = len(word_list) / len(words)

        return {
            'status': 0,
            'data':  {
                'id': reading.id,
                'updated': get_timestamp(reading.updated),
                'status': reading.status,
                'title': reading.title,
                'reading': reading.reading,
                'difficulty': decode_difficulty(reading.difficulty),
                'questions': question_data,
                'files': reading_files,
                'tags': reading_tags_str,
                'stats': {
                    'words': word_list,
                    'total_word': difficulty_score[2],
                    'lexical_diversity': "{0:.3f}".format(lexical_diversity),
                    'total_unique_word': len(word_list),
                    'total_syllable': difficulty_score[3],
                    'total_sentence': difficulty_score[4],
                    'score_1': "{0:.2f}".format(difficulty_score[0]),
                    'score_2': "{0:.2f}".format(difficulty_score[1])
                }
            }
        }

    def insert_new_reading(self, request):
        request_data = request.POST.get('data', None)
        if request_data is None:
            return {'status': 1, 'err_code': 0}

        reading_data = json.loads(request_data)

        if not all(k in reading_data for k in ('reading', 'difficulty')):
            return {'status': 1, 'err_code': 0}

        if len(reading_data['reading']) == 0:
            return {'status': 1, 'err_code': 0}

        print('### DATA OK   ###')
        print('### SAVING... ###')

        new_reading = ReadingMaterial()
        new_reading.title = reading_data['title']
        new_reading.reading = reading_data['reading']
        new_reading.author = request.user
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
            if str(q_index) in request.FILES:
                question_data.tutorial_file = request.FILES[str(q_index)]
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

    def update_reading(self, request, reading, is_admin):
        # Check request data
        request_data = request.POST.get('data', None)
        if request is None:
            return {'status': 1, 'err_code': 1}

        try:
            reading_status = int(request.POST.get('publish', 0))
        except:
            reading_status = 0

        reading_data = json.loads(request_data)

        if not all(k in reading_data for k in ('reading', 'difficulty')):
            return {'status': 1, 'err_code': 1}

        if len(reading_data['reading']) == 0:
            return {'status': 1, 'err_code': 1}

        print('### DATA OK      ###')
        print('### UPDATIING... ###')

        reading.title = reading_data['title']
        reading.reading = reading_data['reading']
        reading.difficulty = encode_difficulty(reading_data['difficulty'])

        if reading_status == 2:
            if is_admin:
                reading.status = 10
            else:
                reading.status = 5
        elif reading_status == 1:
            reading.status = 0
        else:
            if not is_admin:
                reading.status = 0
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

            try:
                vid_temp = NamedTemporaryFile(delete=True)
                vid_temp = urlopen('http://' + request.META['HTTP_HOST'] + q_data.get('tutorial'))
                question_data.tutorial_file.save("video", File(vid_temp))
            except:
                if str(q_index) in request.FILES:
                    question_data.tutorial_file = request.FILES[str(q_index)]
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

    def calculate_reading_content(self, request):
        request_data = request.POST.get('reading', None)
        if request_data is None:
            return {'status': 1, 'err_code': 0}

        reading_data = json.loads(request_data)
        words = re.findall(r'\w+', reading_data.lower())
        word_list = Counter(words).most_common()

        difficulty_score = compute_reading_difficulty(reading_data)

        return {
            'status': 0,
            'data': {
                'stats': {
                    'words': word_list,
                    'total_word': difficulty_score[2],
                    'total_syllable': difficulty_score[3],
                    'total_sentence': difficulty_score[4],
                    'score_1': "{0:.2f}".format(difficulty_score[0]),
                    'score_2': "{0:.2f}".format(difficulty_score[1])
                }
            }
        }
