# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
import models

# Register your models here.
class AvailableTimeAdmin(admin.ModelAdmin):
    list_display = ('user','date','start_from','end_to',)
 
admin.site.register(models.AvailableTime,AvailableTimeAdmin)

class InterviewAdmin(admin.ModelAdmin):
    list_display = ('date','start_from',)
 
admin.site.register(models.Interview,InterviewAdmin)

class AttendsAdmin(admin.ModelAdmin):
    list_display = ('user','status','role','interview')
 
admin.site.register(models.Attends,AttendsAdmin)