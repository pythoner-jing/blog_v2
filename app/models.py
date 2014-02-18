#coding:utf-8
from django.db import models

class User(models.Model):
	username = models.CharField(unique = True, max_length = 20, verbose_name = "用户名")
	register_date = models.DateTimeField(auto_now_add = True, verbose_name = "注册日期")

	def __unicode__(self):
		return self.username

class Tag(models.Model):
	tagname = models.CharField(max_length = 20, unique = True, verbose_name = "标签")

	def __unicode__(self):
		return self.tagname

	class Meta:
		ordering = ["id"]

class Distribute(models.Model):
	link = models.URLField(verbose_name = "链接")
	title = models.CharField(max_length = 50, verbose_name = "标题")
	tags = models.ManyToManyField(Tag, blank = True, verbose_name = "标签")
	date = models.DateTimeField(auto_now_add = True, verbose_name = "发布时间") 
	content = models.TextField(verbose_name = "内容") 
	counter = models.PositiveIntegerField(verbose_name = "访问人数")

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ["-id"]

class Activity(models.Model):
	user = models.ForeignKey(User, verbose_name = "用户名")
	action = models.CharField(max_length = 10, verbose_name = "动作")
	distribute = models.ForeignKey(Distribute, verbose_name = "博文")

	def __unicode__(self):
		return "%s %s %s" % (self.user.username, self.action, self.distribute.title)

	class Meta:
		ordering = ["-id"];

class Motto(models.Model):
	content = models.CharField(max_length = 30, verbose_name = "座右铭")

	def __unicode__(self):
		return self.content
