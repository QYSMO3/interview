# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class AvailableTime(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,)
    date = models.DateField()
    start_from = models.TimeField()
    end_to = models.TimeField()

class Interview(models.Model):
    # attends = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,)
    topics = models.CharField(max_length=64)
    details = models.TextField(blank=True, null=True)
    date = models.DateField()
    start_from = models.TimeField()
    end_to = models.TimeField()

class Attends(models.Model):
	status_choices = (
	                (0, "Pending"),
	                (1, "Yes"),
	                (2, "NO"))

	role_choices = ((0,"candidate"),(1,"interviewer"))

	user = models.ForeignKey(User,on_delete=models.CASCADE,)
	role = models.IntegerField(choices=role_choices,default=1)
	status = models.IntegerField(choices=status_choices,default=0)
	interview = models.ForeignKey(Interview,on_delete=models.CASCADE,)

    


