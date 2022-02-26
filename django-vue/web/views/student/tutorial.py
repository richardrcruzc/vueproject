from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
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


class TutorialView(StudentView):
    def get(self, request, **kwargs):
        question_id = request.GET.get('id', None)

        if question_id == None:
            pass

        try:
            question = ReadingQuestion.objects.get(pk=question_id)
            order = question.order
            difficulty = question.reading_material.difficulty
        except ReadingQuestion.DoesNotExist:
            return {'status': 1, 'error_code': 0}

        print(str(difficulty) + ' ' + str(order))

        full_address = 'https://drive.google.com/open?id=1zGwudsWEBy-T-SPgVYue6mu8eKCXa0cB'
        if difficulty >= 3000 and difficulty < 5000:
            if question.order == 0:
                full_address = 'https://drive.google.com/open?id=1zGwudsWEBy-T-SPgVYue6mu8eKCXa0cB'
            elif question.order == 1:
                full_address = 'https://drive.google.com/open?id=1awBVQjjnEl8sFbMxEFkHw1i6HTnCI6M-'
            elif question.order == 2:
                full_address = 'https://drive.google.com/open?id=122JKK-KGn6vmOXbWTQOeG5Zd95VJfodX'
            else: # question.order == 3:
                full_address = 'https://drive.google.com/open?id=1iaEs-K9LwYvPg5itqfhtYgvSpwt_TX9M'
        elif difficulty >= 5000 and difficulty < 7000:
            if question.order == 0:
                full_address = 'https://drive.google.com/open?id=1W-r-TMTSSnpA1laKWANkWjG_CwMu-wae'
            elif question.order == 1:
                full_address = 'https://drive.google.com/open?id=1QaMLPlwuA8mVPkphkWHnTtaZimsa-jGR'
            elif question.order == 2:
                full_address = 'https://drive.google.com/open?id=1qi7-pkIX0n9mEVlo5q9plG2ZqdTMuuIE'
            else: # question.order == 3:
                full_address = 'https://drive.google.com/open?id=1sAt7D9--HFylzxkrS_-HiJ3krYSaIs2O'

        return HttpResponseRedirect(full_address)
