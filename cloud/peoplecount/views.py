from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from peoplecount.models import Record
from peoplecount.models import Alarm
from django.core import serializers
import json
import datetime

HTTP_OK = HttpResponse('{"status":"OK"}',content_type='application/json')

# Create your views here.
def hello(request): 
	# Hello world 测试
	return HttpResponse("Hello PeopleCount")

# 添加记录
# num: 人头数
def insert(request):
	request.encoding='utf-8'
	if 'num' in request.GET and 'site' in request.GET:
		record = Record(rnum=request.GET['num'], rsite=request.GET['site'])
		record.save()
		return HttpResponse('{"status":"OK"}',content_type='application/json')
	else:
		return HttpResponse('{"status":"ERROR","err":"未指定参数num或site"}')

# 查询一段时间内人流量数据
# earliest: 最早时间戳
# latest: 最晚时间戳
# interval: 时间间隔
def select(request):
	request.encoding='utf-8'
	if 'earliest' in request.GET and 'latest' in request.GET and 'site' in request.GET:
		earliest = datetime.datetime.fromtimestamp(float(request.GET['earliest']))
		latest = datetime.datetime.fromtimestamp(float(request.GET['latest']))
		site = int(request.GET['site'])
		interval = 1
		if 'interval' in request.GET:
			interval = request.GET['interval']
		records = Record.objects.filter(rtime__gte=earliest,rtime__lte=latest,rsite=site)
		records_json = serializers.serialize("json", records)
		return HttpResponse(records_json, content_type='application/json')
	else:
		return HttpResponse('{"status":"ERROR","err":"未指定参数earliest或latest或site"}', content_type='application/json')

# 查询最新的记录
# limit: 查询记录数量
def selectNewest(request):
	limit = 1
	if 'limit' in request.GET:
		limit = int(request.GET['limit'])
	if 'site' in request.GET:
		site = int(request.GET['site'])
		records = Record.objects.filter(rsite=site).order_by('-rid')[0:limit]
		records_json = serializers.serialize('json', records)
		return HttpResponse(records_json, content_type='application/json')
# 获取所有地点最新人数信息
def getLastRecords(request):
	pass

# 添加警告信息
def addAlarm(request):

	request.encoding='utf-8'
	content = ''
	title = ''
	isPop = False
	abnormal = False
	if request.method == 'GET':
		if 'content' in request.GET:
			content = request.GET['content']
		if 'title' in request.GET:
			title = request.GET['title']
		if 'isPop' in request.GET:
			isPop = request.GET['isPop']
		if 'abnormal' in request.GET:
			abnormal = request.GET['abnormal']

		if content is not '' and title is not '':
			alarm = Alarm(acontent=content, aread=False, atitle=title, aPop=isPop, aAbnormal=abnormal)
			alarm.save()
	elif request.method == 'POST':

		filename = ''
		if 'content' in request.POST:
			content = request.POST['content']
		if 'title' in request.POST:
			title = request.POST['title']
		if 'isPop' in request.POST:
			isPop = request.POST['isPop']
		
		img = request.FILES.get('img')
		if img is not None:
			filename = ''
			f = open('static/abnormal/' + filename,'wb')
			for line in img.chunks():
				f.write(line)
			f.close()

		if content is not '' and title is not '':
			alarm = Alarm(acontent=content, aread=False, atitle=title, aimage=filename, aPop=isPop)
			alarm.save()
		
	return HTTP_OK

def selectAlarm(request):
	request.encoding='utf-8'
	if 'limit' in request.GET and 'offset' in request.GET:
		offset = int(request.GET['offset'])
		limit = int(request.GET['limit'])
		alarms = Alarm.objects.all()[offset:limit + offset]
		alarms_json = serializers.serialize('json', alarms)
		return HttpResponse(alarms_json, content_type='application/json')

# 获取弹窗的警告信息
def getPopAlarms(request):
	request.encoding='utf-8'
	alarms = Alarm.objects.filter(aPop=True)
	alarms_json = serializers.serialize('json', alarms)
	return HttpResponse(alarms_json, content_type='application/json')
# 取消弹窗
def cancelPop(request):
	request.encoding='utf-8'
	if 'aid' in request.GET:
		aid = int(request.GET['aid'])
		alarm = Alarm.objects.get(aid=aid)
		alarm.aPop = False
		alarm.aread = True
		alarm.save()
		return HTTP_OK
	else:
		return HttpResponse('{"status":"ERROR","err":"未指定参数aid"}', content_type='application/json')

def unreadAlarm(request):
	request.encoding = 'utf-8'
	alarmNum = int(Alarm.objects.filter(aread=False).count())
	return HttpResponse('{"alarmNum":%d}' % alarmNum, content_type='application/json')

# 批量标为已读
def readAlarms(request):
	if 'ids' in request.GET:
		ids = json.loads(request.GET['ids'])['data']
		for aid in ids:
			alarm = Alarm.objects.get(aid=aid)
			alarm.aread = True
			alarm.save()
		return HTTP_OK
	else:
		return HttpResponse('{"status":"ERROR","err":"未指定参数ids"}', content_type='application/json')

# 将阅读某一条并标为已读
def readAlarm(request):
	if 'id' in request.GET:
		aid = int(request.GET['id'])
		alarm = Alarm.objects.get(aid=aid)
		alarm.aread = True
		print(alarm)
		alarm.save()
		alarm_json = serializers.serialize('json', [alarm])[1:-1]
		return HttpResponse(alarm_json, content_type='application/json')
	else:
		return HttpResponse('{"status":"ERROR","err":"未指定参数id"}', content_type='application/json')
# 批量删除
def deleteAlarms(request):
	if 'ids' in request.GET:
		ids = json.loads(request.GET['ids'])['data']
		for aid in ids:
			alarm = Alarm.objects.get(aid=aid)
			alarm.delete()
		return HTTP_OK
	else:
		return HttpResponse('{"status":"ERROR","err":"未指定参数id"}', content_type='application/json')

def searchAlarm(request):
	request.encoding='utf-8'
	if 'keyword' in request.GET:
		keyword = request.GET['keyword']
		print(keyword)
		alarms = Alarm.objects.filter(Q(atitle__contains=keyword)|Q(acontent__contains=keyword)|Q(atime__contains=keyword)|Q(aid__contains=keyword))
		alarms_json = serializers.serialize('json', alarms)
		return HttpResponse(alarms_json, content_type='application/json')

# 404 与 500错误页面
# def page_not_found(request):
#     return render(request, '404.html')
# def server_error(request):
#     return render(request, '500.html')