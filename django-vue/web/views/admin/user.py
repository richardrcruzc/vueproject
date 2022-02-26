from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from operator import itemgetter
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from types import MethodType
import json

from ..base import AdminView
from arcutils.time_helper import get_timestamp
from arcutils.user_helper import is_admin
from ...models.reading import *
from ...models.student import *
from ...models.teacher import TeacherProfile

from django.contrib.auth.models import User, Group
from django.db import IntegrityError

# ---------change----
from ...models.data import *
# ---------end-------


class AdminUserView(AdminView):
    def get(self, request, **kwargs):
        self.set_page('user', 'Senarai Pengguna')

        if 'page_action' in kwargs:
            if is_admin(request):
                if kwargs['page_action'] == 'add':
                    self.set_page('user', 'Add User')
                    return self.render(request, 'arc/admin/user-form.html')
                elif kwargs['page_action'] == 'edit':
                    self.set_page('user', 'Edit User')
                    return self.render(request, 'arc/admin/user-form.html')
                elif kwargs['page_action'] == 'delete':
                    target_page = int(request.GET.get('page', 0))
                    User.objects.filter(pk=request.GET.get('id', -1)).delete()
                    if target_page > 0:
                        return redirect('/user' + ('?page=' + str(target_page)))

            if kwargs['page_action'] == 'detail':
                self.set_page('user', 'Detail')
                if 'id' in request.GET:
                    student_id = request.GET['id']
                    student_report = StudentReport.objects.filter(student_id=student_id).all()

                    student_details = []
                    for quiz_material in student_report:
                        #test_report = ReportDetail.objects.filter(student_report=test).all()
                        questions = ReadingQuestion.objects.filter(reading_material=quiz_material.reading)
                        qreport_data = []
                        for question in questions:
                            total_trial = ReportDetail.objects.filter(student_report=quiz_material, question=question).count()
                            qreport_data.append({'trial': total_trial})

                        student_details.append({
                            'level': "{0:.2f}".format(quiz_material.reading.difficulty/1000), # + "/" + str(quiz_material.reading.id),
                            'report': qreport_data,
                            'ts': get_timestamp(quiz_material.taken)
                        })

                    self.context.update({'student_details': student_details})
                return self.render(request, 'arc/admin/user-detail.html')
            return redirect('user-list')
        else:
            is_superuser = is_admin(request)
            class_required = False
            if is_superuser:
                group_id = request.GET.get('group_id')
                if group_id is None:
                    group_id = 100
                gp = group_id
                st_d = grade_info.objects.filter(grade=gp).values('start_date')
                en_d = grade_info.objects.filter(grade=gp).values('end_date')
                users = User.objects.filter(is_superuser=0, date_joined__gte=st_d, date_joined__lt=en_d).order_by('username').all()
                # users = User.objects.filter(is_superuser=0).order_by('username').all()
            else:
                if request.user.teacher_profile.classrooms.count() == 1:
                    selected_class = request.user.teacher_profile.classrooms.first()
                else:
                    try:
                        selected_class_id = int(request.GET.get('class', -1))
                        selected_class = Classroom.objects.get(id=selected_class_id)
                        class_required = True
                    except Exception as ex:
                        all_classroom = [{'id': classroom.id, 'name': classroom.name} for classroom in request.user.teacher_profile.classrooms.all()]
                        self.context.update({'classrooms': all_classroom})
                        return self.render(request, 'arc/admin/user-list-classroom.html')

                all_students_id = [profile.student.id for profile in selected_class.students.all()]

                users = User.objects.filter(id__in=all_students_id).order_by('username').all()

            user_list = []
            paginator = Paginator(users, self.NUM_PAGES)

            try:
                shown_users = paginator.page(request.GET.get('page', 1))
            except (ValueError, PageNotAnInteger):
                shown_users = paginator.page(1)
            except (EmptyPage, InvalidPage):
                shown_users = paginator.page(paginator.num_pages)

            for user in shown_users.object_list:
                fullname = ''
                rank = -1
                state = ''
                # grade = 0
                try:
                    profile = StudentProfile.objects.get(student=user)
                    fullname = profile.fullname
                    rank = profile.rank
                    # change
                    state = user.is_active
                except:
                    try:
                        profile = TeacherProfile.objects.get(teacher=user)
                        fullname = profile.fullname
                        # change
                        state = user.is_active
                    except:
                        print('No profile:', user)

                user_data = {
                    'id': user.pk,
                    'username': user.username,
                    'name': fullname.title(),
                    'rank': rank,
                    'last_login': get_timestamp(user.last_login),
                    'created': get_timestamp(user.date_joined),
                    # change
                    'state': state,
                    # 'grade': grade
                }


                user_group = user.groups.first()
                if user_group is not None:
                    user_group_name = user_group.name.lower()
                    user_role = -1
                    if user_group_name == 'admin':
                        user_role = 0
                    elif user_group_name == 'teacher':
                        user_role = 1
                    elif user_group_name == 'student':
                        user_role = 2
                    user_data.update({'role': user_role})

                user_list.append(user_data)

            if not request.user.groups.filter(name__in=['admin']).exists():
                sorted_user = sorted(user_list, key=lambda i: i['rank'], reverse=True)
                prev_score = -1
                prev_rank = -1
                for idx, current_user in enumerate(sorted_user):
                    for target_user in user_list:
                        if target_user['id'] == current_user['id']:
                            if prev_score > -1 and prev_score == target_user['rank']:
                                target_user['rank'] = prev_rank
                            else:
                                prev_score = target_user['rank']
                                target_user['rank'] = idx + 1
                                prev_rank = idx + 1

                            break

            self.context.update({'user_data': user_list})

            shown_pages = 2

            # check first page
            paginator_range_first = shown_users.number - shown_pages
            if paginator_range_first < 3:
                # shown_pages = shown_pages + (1 - paginator_range_first)
                paginator_range_first = 1
                paginator_range_last = 2 * shown_pages + 1
            else:
                paginator_range_last = shown_users.number + shown_pages

            if paginator_range_last > paginator.num_pages:
                paginator_range_last = paginator.num_pages
            elif paginator_range_last == paginator.num_pages - 1:
                paginator_range_last = paginator.num_pages
                paginator_range_first = paginator_range_first + 1


            pagination_data = {
                'start_index': shown_users.start_index(),
                'end_index': shown_users.end_index(),
                'has_next': shown_users.has_next(),
                'has_other_pages': shown_users.has_other_pages(),
                'has_previous': shown_users.has_previous(),
                'number': shown_users.number,
                'per_page': paginator.per_page,
                'shown_pages': [paginator_range_first, paginator_range_last],
                'total_page': paginator.num_pages,
                'total_items': paginator.count
            }

            self.context.update({'pagination': pagination_data})
            if class_required:
                self.context.update({'filter_template': 'class=' + str(selected_class_id)})

            if is_superuser:
                groups = grade_info.objects.all()
                group_int = (int)(group_id)
                self.context.update({'groups': groups})
                self.context.update({'group_id': group_id})
                self.context.update({'group_int': group_int})
                return self.render(request, 'arc/admin/user-list.html')
            else:
                return self.render(request, 'arc/admin/user-list-teacher.html')

    def post(self, request, **kwargs):
        if 'page_action' in kwargs:
            if kwargs['page_action'] == 'add':
                retval = self.insert_new_user(request)

                if retval['status'] == 0:
                    return JsonResponse(retval)
                else:
                    return JsonResponse({
                        'status': retval['status'] + retval.get('error_code', 0),
                        'err': 'Invalid data'})
            elif kwargs['page_action'] == 'edit':
                user_id = request.GET.get('id', 0)
                request_type = 'request'
                if 'params' in request.POST:
                    params_data = json.loads(request.POST['params'])
                    request_type = params_data.get('type', 'request')

                if request_type == 'request':
                    retval = self.retrieve_user(request, user_id)
                    if retval['status'] == 0:
                        return JsonResponse(retval)
                    else:
                        return JsonResponse({
                            'status': retval['status'] + retval.get('error_code', 0),
                            'err': 'No valid data'})
                elif request_type == 'save':
                    retval = self.update_user(request, user_id)
                    if retval['status'] == 0:
                        return JsonResponse(retval)
                    else:
                        return JsonResponse({
                            'status': retval['status'] + retval.get('error_code', 0),
                            'err': 'No valid data'})
            elif kwargs['page_action'] == 'reset':
                user_id = request.GET.get('id', 0)

                retval = self.reset_user(request, user_id)
                if retval['status'] == 0:
                    return JsonResponse(retval)
                else:
                    return JsonResponse({
                        'status': retval['status'] + retval.get('error_code', 0),
                        'err': 'No valid data'})

        return JsonResponse({'status': 1, 'err': 'Invalid action'})

    def insert_new_user(self, request):
        request_data = request.POST.get('data', None)
        if request_data is None:
            return {'status': 1, 'err_code': 0}

        user_data = json.loads(request_data)
        if not all(k in user_data for k in ('username', 'password', 'role')):
            return {'status': 1, 'err_code': 0}

        if len(user_data['username']) == 0 or len(user_data['username'].strip()) == 0:
            return {'status': 1, 'err_code': 0}

        if len(user_data['password']) == 0:
            return {'status': 1, 'err_code': 0}

        print('### DATA OK   ###')
        print('### SAVING... ###')

        new_user = User()
        new_user.username = user_data['username'].strip().lower()
        new_user.set_password(user_data['password'])
        try:
            new_user.save()
        except IntegrityError:
            return {'status': 1, 'err_code': 1}

        user_role = int(user_data['role'])

        try:
            if user_role == 0:
                group = Group.objects.get(name='admin')
            elif user_role == 1:
                group = Group.objects.get(name='teacher')
            else:
                group = Group.objects.get(name='student')
        except Group.DoesNotExist:
            group = Group()
            if user_role == 0:
                group.name = 'admin'
            elif user_role == 1:
                group.name = 'teacher'
            elif user_role == 2:
                group.name = 'student'
            group.save()

        new_user.groups.add(group)
        if user_role == 2:
            # Create student profile
            student_profile = StudentProfile()
            student_profile.student = new_user
            student_profile.save()
        return {
            'status': 0,
            'data': {'id': new_user.id}
        }

    def retrieve_user(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return {'status': 1, 'error_code': 0}

        user_data = {
            'id': user.pk,
            'username': user.username,
            'last_login': get_timestamp(user.last_login),
            'created': get_timestamp(user.date_joined)
        }
        user_group = user.groups.first()
        if user_group is not None:
            user_group_name = user_group.name.lower()
            user_role = -1
            if user_group_name == 'admin':
                user_role = 0
            elif user_group_name == 'teacher':
                user_role = 1
            elif user_group_name == 'student':
                user_role = 2

            user_data.update({'role': user_role})

        return {
            'status': 0,
            'data': user_data
        }

    def update_user(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return {'status': 1, 'error_code': 0}

        # Check request data
        request_data = request.POST.get('data', None)
        if request is None:
            return {'status': 1, 'err_code': 1}

        user_data = json.loads(request_data)

        if not all(k in user_data for k in ('password', 'role')):
            return {'status': 1, 'err_code': 1}

        if len(user_data['password']) == 0:
            return {'status': 1, 'err_code': 1}

        print('### DATA OK      ###')
        print('### UPDATIING... ###')

        user.set_password(user_data['password'])
        user.save()

        user_role = int(user_data['role'])
        try:
            if user_role == 0:
                group = Group.objects.get(name='admin')
            elif user_role == 1:
                group = Group.objects.get(name='teacher')
            else:
                group = Group.objects.get(name='student')
        except Group.DoesNotExist:
            group = Group()
            if user_role == 0:
                group.name = 'admin'
            elif user_role == 1:
                group.name = 'teacher'
            elif user_role == 2:
                group.name = 'student'
            group.save()

        user.groups.clear()
        user.groups.add(group)

        return {
            'status': 0,
            'data': { 'id': user.id }
        }

    def reset_user(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return {'status': 1, 'error_code': 0}

        # Reset password

        user.set_password(user.username)
        user.save()

        if user.groups.filter(name__in=['admin', 'teacher']).exists():
            profile = TeacherProfile.objects.filter(teacher=user).first()
        else:
            profile = StudentProfile.objects.filter(student=user).first()

        if profile:
            profile.change_password = True
            profile.save()

        return { 'status': 0 }