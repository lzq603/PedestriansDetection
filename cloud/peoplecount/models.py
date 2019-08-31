from django.db import models

# Create your models here.
class Record(models.Model):
	# 记录id
	rid = models.AutoField(primary_key=True)
	# 检测到人头数
	rnum = models.IntegerField()
	# 时间
	rtime = models.DateTimeField(auto_now=True)
	# 地点
	rsite = models.IntegerField()

class Config(models.Model):
	"""配置信息"""
	ckey = models.CharField(primary_key=True,max_length=20)
	cvalue = models.CharField(max_length=20)

class Site(models.Model):
	# 地点id
	sid = models.AutoField(primary_key=True)
	# 地点名称
	sname = models.CharField(max_length=50)
	# 报警阈值
	salarm = models.IntegerField()
	# 负责人
	sprincipal = models.CharField(max_length=50)
	# 负责人联系方式
	sphone = models.CharField(max_length=50)
	# 此地点人流量爆发次数
	sbreakout = models.IntegerField()
	# 此地点所使用的算法
	sarithmetic = models.CharField(max_length=50)

class Alarm(models.Model):
	# 报警id
	aid = models.AutoField(primary_key=True)
	# 标题
	atitle = models.CharField(max_length=255)
	# 警报内容
	acontent = models.CharField(max_length=255)
	# 报警时间
	atime = models.DateTimeField(auto_now=True)
	# 是否已读
	aread = models.BooleanField()
	# 图片记录
	aimage = models.CharField(max_length=255)
	# 弹框 (True表示弹窗信息且未弹出)
	aPop = models.BooleanField()
	# 是否异常行为
	aAbnormal = models.BooleanField()
	# 附带视频
	aVideo = models.CharField(max_length=255)