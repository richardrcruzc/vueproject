from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from arcutils.path import *
import os
import time

class final_test_state(models.Model):
    class Meta:
        db_table = 'final_test_state'

    created = models.DateTimeField(auto_now_add=True)
    state = models.BooleanField()
