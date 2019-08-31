# -*- coding: utf-8 -*-
# @Author: lizhiqag@163.com
# @Date:   2019-05-03 09:01:24
# @Description   [ description ]
# @Last Modified time: 2019-06-05 10:08:11

import cv2 as cv
import numpy as np
import base64
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pedestrian_detect.detector import detect
from peoplecount.models import Config
from peoplecount.models import Site
from peoplecount.models import Alarm

HTTP_OK = HttpResponse('{"status":"OK"}',content_type='application/json')

# Web端页面接口
def hello(request):
	return HttpResponse('Hello world !')

def login(request):
	context = {}
	context['hello'] = 'Hello world'
	return render(request,'login.html',context)

def index(request):
	return render(request,'index.html')

def monitor(request):
	return render(request,'monitor.html')

@csrf_exempt
def login_do(request):
	request.encoding='utf-8'
	context = {'err':'密码错误'}
	print(request.POST['username'], request.POST['password'])
	if 'username' in request.POST and 'password' in request.POST:
		if request.POST['username'] == '图南队' and request.POST['password'] == 'admin':
			return render(request,'index.html')
		else:
			return render(request,'login.html',context)
	else:
		return render(request,'error.html')

def register(request):
	return render(request,'register.html')

def home(request):
	return render(request,'home.html')

def setting(request):
	return render(request,'setting.html')

def siteThreshold(request):
	if 'site' in request.GET:
		sid = request.GET['site']
		context = {'sid':sid}
		return render(request,'siteThreshold.html',context)
	else:
		return HttpResponse('{"status":"ERROR","err":"未指定参数site"}', content_type='application/json')

def analyze(request):
	return render(request,'analyze.html')

def alarmMsg(request):
	return render(request,'alarmMsg.html')

def exception(request):
	return render(request,'exception.html')

def alarmContent(request):
	if 'id' in request.GET:
		aid = int(request.GET['id'])
		alarm = Alarm.objects.get(aid=aid)
		alarm.aread = True
		alarm.save()
		context = {'alarm':alarm}
		return render(request,'alarmContent.html',context)
	else:
		return HttpResponse('{"status":"ERROR","err":"未指定参数id"}', content_type='application/json')

def detail(request):
	if 'site' in request.GET:
		sid = int(request.GET['site'])
		site = Site.objects.get(sid=sid)
		context = {'site':site}
		return render(request,'detail.html',context)
	else:
		return HttpResponse('{"status":"ERROR","err":"未指定参数sid"}', content_type='application/json')

def blank(request):
	return render(request,'blank.html')


# JSON数据接口
# 获取检测阈值
def getConfig(request):
	config = Config.objects.all()
	config_json = serializers.serialize('json',config)
	return HttpResponse(config_json,content_type='application/json')

# 获取地点信息
def getSites(request):
	sites = Site.objects.all()
	sites_json = serializers.serialize('json',sites)
	return HttpResponse(sites_json,content_type='application/json')

def setAlarm(request):
	if 'site' in request.GET and 'alarmThreshold' in request.GET:
		site = int(request.GET['site'])
		alarmThreshold = int(request.GET['alarmThreshold'])
		site = Site.objects.get(sid=site)
		site.salarm = alarmThreshold
		site.save()
		return HttpResponse('{"status":"OK"}',content_type='application/json')
	else:
		return HttpResponse('{"status":"ERROR","err":"缺少参数site或alarmThreshold"}',content_type='application/json')

# 设置检测阈值
def setScoreThreshold(request):
	if 'score' in request.GET:
		score = float(request.GET['score'])
		img = cv.imread('static/TestImages/' + 'example.jpg')

		rectangles = detect(img,scoreThreshold=score)
		print('人头数：',len(rectangles))
		i = 1
		for rect in rectangles:
			x,y,x2,y2,score = int(rect[0]), int(rect[1]), int(rect[2]), int(rect[3]), rect[4]
			# cv.putText(img, str(round(score,4)), (x, y), cv.FONT_HERSHEY_PLAIN, 1, (0xFF,0xFF,0xFF), 2)
			cv.putText(img, str(i),(x,y),cv.FONT_HERSHEY_PLAIN, 1, (0xFF,0xFF,0), 2)
			cv.rectangle(img,(x,y),(x2,y2),(0,0xFF,0xFF),2)
			i+=1
			# print(x,y,x2-x,y2-y,':',score)
		
		# image = cv.imencode('.jpg',img)[1]
		# imgbase64 = base64.b64encode(image)
		cv.imwrite('static/temp.png',img)
		with open('static/temp.png', 'rb') as f:
			image_data = f.read()

		# 更新数据库
		config = Config.objects.get(ckey='scoreThreshold')
		config.cvalue = request.GET['score']
		config.save()
		return HttpResponse(image_data,content_type='image/png')
	else:
		return HttpResponse('缺少必要的参数score')

@csrf_exempt
def changeTestImage(request):
	if request.method == 'POST':
		img = request.FILES.get('img')
		f = open('static/TestImages/' + 'example.jpg','wb')
		for line in img.chunks():
			f.write(line)
		f.close()
		return HTTP_OK