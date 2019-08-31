# -*- coding: utf-8 -*-
# @Author: lizhiqag@163.com
# @Date:   2019-05-03 09:26:59
# @Description   [ description ]
# @Last Modified time: 2019-05-30 23:08:49
from django.urls import path, include
from peoplecount import views

urlpatterns = [
	path('hello/',views.hello),
	path('insert/',views.insert),
	path('select/',views.select),
	path('selectNewest/',views.selectNewest),
	path('addAlarm/',views.addAlarm),
	path('selectAlarm/',views.selectAlarm),
	path('searchAlarm/',views.searchAlarm),
	path('unreadAlarm/',views.unreadAlarm),
	path('readAlarm/', views.readAlarm),
	path('readAlarms/', views.readAlarms),
    path('deleteAlarms/', views.deleteAlarms),
    path('getPopAlarms/', views.getPopAlarms),
    path('cancelPop/', views.cancelPop)
]


# handler404 = views.page_not_found
# handler500 = views.server_error