from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from django.template import Library
from json import dumps as json_dumps
from django.shortcuts import get_object_or_404, render, redirect

from ..base import AdminView
from arcutils.time_helper import get_timestamp
from arcutils.user_helper import is_admin
from ...models.reading import *
from ...models.student import *

from ...models.teacher import TeacherProfile

from django.contrib.auth.models import User, Group
from django.db import IntegrityError

from ...models.data import *
from ...models.test import *

def active(request):
    grade_id = (int)(request.GET.get('grade'))
    sd = grade_info.objects.filter(grade=grade_id).values('start_date')
    ed = grade_info.objects.filter(grade=grade_id).values('end_date')
    if grade_id is 100:
        User.objects.filter(is_superuser=0).update(is_active=1)
    else:
        User.objects.filter(date_joined__gte=sd, date_joined__lt=ed, is_superuser=0).update(is_active=1)
    return HttpResponse(grade_id)

def archive(request):
    grade_id = (int)(request.GET.get('grade'))
    sd = grade_info.objects.filter(text=grade_id).values('start_date')
    ed = grade_info.objects.filter(text=grade_id).values('end_date')
    if grade_id is 100:
        User.objects.filter(is_superuser=0).update(is_active=0)
    else:
        User.objects.filter(date_joined__gte=sd, date_joined__lt=ed, is_superuser=0).update(is_active=0)
    return HttpResponse(grade_id)

def add_group(request):
    group = (int)(request.GET.get('group'))
    ex_g = grade_info.objects.filter(grade=group).first()
    if ex_g:
        return HttpResponse()
    sd = datetime(group, 1, 1, 0, 0, 0)
    ed = datetime(group+1, 1, 1, 0, 0, 0)
    text = (str)(group)
    new_group = grade_info(grade=group, text=text, start_date=sd, end_date=ed)
    new_group.save()
    return HttpResponse(group)

def upload_csv(request):
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            # this is not csv file
            return HttpResponseRedirect('/user')
        if csv_file.multiple_chunks():
            # messages.error(request, "Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))
            return HttpResponseRedirect('/user')

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\n")
        # loop over the lines and save them in db. If error , store as string and then display
        for line in lines:
            fields = line.split(",")
            data_dict = {}
            if fields[0] == '':
                return HttpResponseRedirect('/user')
            data_dict["name"] = fields[2]
            data_dict["username"] = fields[0]
            data_dict["password"] = fields[1]
            ex_users = User.objects.filter(username=data_dict['username']).count()
            if ex_users is 0:
                user = User.objects.create_user(data_dict["username"], data_dict["name"], data_dict["password"])
                user.groups.add(2)
                user.save()
        return HttpResponseRedirect('/user')

def state(requset):
    userid = requset.GET['userid']
    user_state = requset.GET['state']
    User.objects.filter(id=userid).update(is_active=user_state)
    return HttpResponse(userid)

def change_state(request):
    name = request.GET.get('id')
    is_active = request.GET.get('state')
    User.objects.filter(username=name).update(is_active=is_active)
    return HttpResponse(is_active)

def activate_record(reqest):
    act = reqest.GET.get('act')
    new_act = final_test_state(state=act)
    new_act.save()
    return HttpResponse(act)

def delete_group(request):
    gp_id = (int)(request.GET.get('group_id'))
    grade_info.objects.filter(grade=gp_id).delete()
    return HttpResponseRedirect('/user')



