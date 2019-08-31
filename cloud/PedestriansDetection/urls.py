"""WebFlow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
# from django.conf.urls import static
from django.views import static ##新增
from django.conf import settings ##新增
from django.conf.urls import url
# from PedestriansDetection.settings import STATIC_URL, STATIC_ROOT
from . import view

urlpatterns = [
	# path('admin/', admin.site.urls),

	# JSONs数据接口
	path('hello/', view.hello),
	path('peoplecount/', include('peoplecount.urls')),
	path('alram/', include('peoplecount.urls')),
	path('setScoreThreshold/', view.setScoreThreshold),
	path('changeTestImage', view.changeTestImage),
	path('getConfig/', view.getConfig),
	path('getSites/', view.getSites),
	path('setAlarm/', view.setAlarm),

	# Web端页面接口
	path('index/', view.index),
	path('login/', view.login),
	path('login_do/', view.login_do),
	path('register/', view.register),
	path('home/', view.home),
	path('alarmMsg/', view.alarmMsg),
	path('alarmContent/', view.alarmContent),
	path('monitor/', view.monitor),
	path('setting/', view.setting),
	path('analyze/', view.analyze),
	path('exception/', view.exception),
	path('siteThreshold/', view.siteThreshold),
	path('blank/', view.blank),
	path('detail/', view.detail),

	# 访问静态资源
	url(r'^static/(?P<path>.*)$', static.serve,
      {'document_root': settings.STATIC_ROOT}, name='static'),
]


# urlpatterns += static.static(STATIC_URL, document_root=STATIC_ROOT)
