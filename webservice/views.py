# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.core import serializers
import logging
import models
import datetime
import json
import logging

logger = logging.getLogger(__name__)
# Create your views here.

# ==================not main API, apis to help for testing=============================
Successful_response = {'status':'200','messages':'success','data':''}

# function to show index page
def index(request):
    Users = User.objects.all()
    ids = {}
    for i in Users:
        ids[i.id]=i.username
    return render(request, 'index.html',{'Users': Users,'ids':ids})

# function to show a user's time
def times(request,ID):
    user = get_object_or_404(User,pk=ID)
    available_time = models.AvailableTime.objects.filter(user=user)
    attends = models.Attends.objects.filter(user=user)
    return render(request, 'times.html',{'user': user,'available_time':available_time,'attends':attends})

# function to create a new user
def users(request):
    if request.method == 'POST':
        userName = request.POST.get('username', None)
        if userName:
           created = User.objects.create_user(userName)
           if created:
              # user was created
              return JsonResponse({'status':'200','messages':'success','data':''})
           else:
              logger.error('Failed to create user',exc_info  = True)
              return HttpResponseBadRequest('Failed')
        else:
           return HttpResponseBadRequest('None')
    else:
        return HttpResponseNotAllowed(['POST'])


#  function to arrange a interview,the earliest possible one
def interviews(request):
    if request.method == 'POST':
        c = request.POST.get('c',None)
        i_list = request.POST.getlist('i',None)
        if c and i_list:
            candidate = get_object_or_404(User, pk=c[0])
            interviewer_list=[]
            for i in i_list:
                interviewer_list.append(get_object_or_404(User, pk=i))
            available_times = find_available_time(c,i_list)
            #like  {date1:[(start,to),(start,to)],date2:[(start,to)]}
            if available_times:
                date = available_times.keys()[0]
                time = available_times[date][0].split('-') # available_times[date] like [u'7:00-8:00', u'8:00-9:00']
                start_from = datetime.time(int(time[0].split(":")[0]))
                end_to = datetime.time(int(time[1].split(":")[0]))
                #create the interview obj
                I = models.Interview(topics=candidate.username,date=date,start_from=start_from,end_to=end_to)
                I.save()
                #create the attend obj
                a_C = models.Attends(user=candidate,role=0,interview=I)
                a_C.save()
                for i in interviewer_list:
                    a_I = models.Attends(user=i,interview=I)
                    a_I.save()
                return JsonResponse(Successful_response)
            else:
                return HttpResponseBadRequest('No available time')
        else:
            return HttpResponseBadRequest('need one candidate and at least one interviewer')
    else:
        return HttpResponseBadRequest('Unsupported method')

#  function to add a new available time for a user
def availables(request):
    if request.method == 'POST':
        ID = request.POST.get('userID',None)
        date = request.POST.get('date',None)
        start_from = request.POST.get('start',None)
        end_to = request.POST.get('end',None)
        if ID and date and start_from and end_to:
            user = get_object_or_404(User, pk=ID)
            try:
                a = models.AvailableTime(user=user, date=date, start_from=start_from, end_to=end_to)
                a.save()
                return JsonResponse(Successful_response)
            except Exception,e:
                logger.error(e,exc_info  = True)
        else:
            return HttpResponseBadRequest('not enough information')

    else:
        return HttpResponseNotAllowed(['POST'])

# ==================main API, the API to show possible interview times ================
def api_available_times(request):
    if request.method == 'GET':
        c = request.GET.getlist('c')
        i_list = request.GET.getlist('i')
        # only one candidate is allowed
        if len(c)>1:
            return HttpResponseBadRequest('only one candidate needed')
        elif len(c)==0:
            return HttpResponseBadRequest('need one candidate')
        else:
            pass
        if len(i_list)<=0:
            return HttpResponseBadRequest('need at least one i')


        available_times = find_available_time(c[0],i_list)
        Successful_response['data'] = available_times
        return JsonResponse(Successful_response)
    else:
        return HttpResponseNotAllowed(['GET'])

def find_available_time(c,i_list):
    """ 
    function to find the possible interview times
    return data like {"2018-08-11": ["8:00-9:00", "9:00-10:00"]}
    """
    candidate = get_object_or_404(User, pk=c[0])
    interviewer_list = []
    for i in i_list:
        interviewer_list.append(get_object_or_404(User, pk=i))

    available_times={} #{date1:[(start,to),(start,to)],date2:[(start,to)]}
    # find out candidate's available time
    available_times = query_to_dict(models.AvailableTime.objects.filter(user=candidate))
    c_interviews = query_to_dict(models.Interview.objects.filter(attends__user=candidate).exclude(attends__status=2))
    available_times = match_querys(available_times,available_times,c_interviews)

    for interviewer in interviewer_list:
        i_query = query_to_dict(models.AvailableTime.objects.filter(user=interviewer))
        a_query = query_to_dict(models.Interview.objects.filter(attends__user=interviewer).exclude(attends__status=2))
        available_times = match_querys(available_times,i_query,a_query) 
    _available_times = {}
    for i in available_times: 
        # available_times like {date1:[(start,to),(start,to)],date2:[(start,to)]}
        # i like date1
        # store the available slots in the day
        _l = []
        for s in available_times[i]:
            # available_times[i] like [(start,to),(start,to)]
            # change a time slot into full hours e.g. 6:01~8:00 --> 7:00~8:00
            fianl_slot = get_full_time(s)
            _l+=fianl_slot
        if _l:
            _available_times[i.strftime('%Y-%m-%d')] = _l

    return _available_times

def get_full_time(s):
    """
    change a time slot into full hours 
    e.g. 6:01~9:00 --> 7:00~8:00,8:00~9:00
    s like (t1,t2)
    """
    final_list = []
    t1=s[0]
    t2=s[1]
    if t1.minute==0 and t1.second==0:
        h1=s[0].hour
    else:
        h1=s[0].hour+1
    h2 = t2.hour

    # 
    if h2<=h1 or h1>23:
        return []
    else:
        for i in range(h1,h2):
            t="%d:00-%d:00"%(i,i+1)
            final_list.append(t)
    return final_list

def query_to_dict(q):
    d = {}
    for i in q:
        if d.has_key(i.date):
            d[i.date].append((i.start_from,i.end_to))
        else:
            d[i.date]=[(i.start_from,i.end_to)]
    return d

def match_times(slot,time_list):
    """
    Comapre a single slot t1~t2 with a list of slots t3~t4,t5~t6
    Compare single slot with each element of the list
    whole list is   (t1,t2) , [(t3,t4),(t5,t6),(t7,t8)]
    1. (t1,t2)|(t3,t4)  -->result1
    2. (t1,t2)|(t4,t5)  -->result1
    .................
    result = [result1,result2]

    slot format:(t1,t2)
    time_list format: [(t1,t2),(t3,t4)]
    e.g. [(datetime.time(6, 1, 2), datetime.time(8, 0)),(datetime.time(9, 1, 2), datetime.time(18, 0))]
    """
    available_list = []
    for i in time_list:  # i like (t1, t2)
        print 'i is',i
        print 'slot is',slot
        latest_start = max(slot[0],i[0])
        earliest_end = min(slot[1],i[1])
        if latest_start<earliest_end:
            available_list.append((latest_start,earliest_end))
    return available_list

def match_querys(available_times,interviewer_times,interviews):
    """
    Compare the current available time slots wiht the time of interviewer
    two arguemant have the same format.
    format:    {d1:[(t1,t2),(t3,t4)],d2:[(t5,t6)]}
    e.g. 
    {datetime.date(2018, 8, 11): [(datetime.time(6, 1, 2), datetime.time(18, 0))]}
    available times:  {d1:[(t1,t2),(t3,t4)],d2:[(t5,t6)]}
    interviewer_times: {d1:[(T1,T2),(T3,T4)]}

    1. starting from comparing each day,    
        e.g. d1
        [(t1,t2),(t3,t4)] v.s. [(T1,T2),(T3,T4)]

    2. for each slot in available times of the day, comapre with the interviews list:
        (t1,t2) | [(T1,T2),(T3,T4)] --> [(t1,t2)] 
        (t3,t4) |[(T1,T2),(T3,T4)]  --> slot2 does not match
        result1 = {d1:[slot1]}

    3. compare the next day
    ............

    finally return {d1:[(t1,t2)]}

    """
    d={}
    # compare candidate's time day by day.
    print 'a is',available_times
    for day in available_times:  #e.g. [(t1,t2),(t3,t4)]
        slot_list=[]
        # [(t1,t2),(t3,t4)] v.s. [(T1,T2),(T3,T4)]
        if interviewer_times.has_key(day):
            # (t1,t2) | [(T1,T2),(T3,T4)]
            # (t3,t4) | [(T1,T2),(T3,T4)]
            for slot in available_times[day]:  #e.g. (t1,t2)
                mached = match_times(slot,interviewer_times[day])
                # take the time off if there's a interview
                if interviews.has_key(day):
                    mached = cut_slots(mached,interviews[day])
                slot_list+=mached
            
        # {d1:[slot1,slot2]}
        if slot_list:
            if d.has_key(day):
                d[day] += slot_list
            else:
                d[day] = slot_list
    return d

def cut_slots(slots1,slots2):
    """
    checkt if slot2 in slot1, and return the slot without slot2
    format [(t1,t2)], [(T1,T2),(T3,T4)]
    if slot2 in the peroid of slot1, cut slot1 into 2 pieces, not containing the slot2
    e.g. slot1 is (9am,10pm), slot2 is [(11am,2pm),(3pm,4pm)]
    1. (9am,10pm) v.s. (11am,2pm) --> [(9am,11am),(2pm,10pm)]
    2. [(9am,11am),(2pm,10pm)] v.s. (3pm,4pm) --> [(9am,11am),(2pm,3pm),(4pm,10pm)]
    3. result is [(9am,11am),(2pm,3pm),(4pm,10pm)]
    
    (t1,t2) v.s. (t3,t4)
    No need to cut if slot2 not in slot1: t2<=t3 or t1>=t4     
    """
    l = slots1
    for s2 in slots2:
        # l=[cut_times(i,s2) for i in l]
        _l = []
        for i in l:
            _l+=cut_times(i,s2)
        l=_l

    return l


def cut_times(slot1,slot2):
    # (t1,t2) v.s. (t3,t4)
    # No need to cut if slot2 not in slot1: t2<=t3 or t1>=t4     
    d=[]
    t1=slot1[0]
    t2=slot1[1]
    t3=slot2[0]
    t4=slot2[1]
    if t2<=t3 or t1>=t4:
        return [slot1]
    if t1==t3 and t2==t4:
        return d
    if t1<=t3:
        if t2>=t4:
        # t1<=t3 & t2>=t4  => t1~t3,t4~t2
            d=[(t1,t3),(t4,t2)]
        else: 
        #t1<=t3 & t2<t4 =>t1~t3
            d=[(t1,t3)]
    else:  #t1>t3
        if t2>=t4:
        # t1>t3 & t2>=t4
            d=[(t4,t2)]
        else: 
        #t1>t3 & t2<t4
            d=[]
    return d

