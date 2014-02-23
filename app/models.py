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
	title = models.CharField(max_length = 50, verbose_name = "标题")
	tags = models.ManyToManyField(Tag, blank = True, verbose_name = "标签")
	date = models.DateTimeField(auto_now_add = True, verbose_name = "发布时间") 
	content = models.TextField(verbose_name = "内容") 

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ["-id"]

class Activity(models.Model):
	user = models.ForeignKey(User, verbose_name = "用户")
	action = models.CharField(max_length = 10, verbose_name = "动作")
	distribute = models.ForeignKey(Distribute, verbose_name = "博文")

	def __unicode__(self):
		return "%s %s %s" % (self.user.username, self.action, self.distribute.title)

	class Meta:
		ordering = ["-id"]

class Motto(models.Model):
	content = models.CharField(max_length = 30, verbose_name = "座右铭")

	def __unicode__(self):
		return self.content

class Comment(models.Model):
	distribute = models.ForeignKey(Distribute, verbose_name = "评论博文")
	user = models.ForeignKey(User, verbose_name = "用户") 
	content = models.TextField(verbose_name = "评论")
	ref = models.ForeignKey("Comment", blank = True, null = True, verbose_name = "引用")
	date = models.DateTimeField(auto_now_add = True, verbose_name = "评论时间") 

	def __unicode__(self):
		return "%s %s" % (self.user.username, self.content)

	class Meta:
		ordering = ["-date"]

class Record(models.Model):
	year = models.PositiveIntegerField(verbose_name = "年份")
	month = models.PositiveIntegerField(verbose_name = "月份")

	def __unicode__(self):
		return unicode(self.year) + u"年" + unicode(self.month) + u"月"

	class Meta:
		ordering = ["year", "month"] 

class Count(models.Model):
	distribute = models.ForeignKey(Distribute, verbose_name = "文章")
	ip = models.CharField(max_length = 20, verbose_name = "ip地址")

	def __unicode__(self):
		return "%s %s" % (self.distribute.title, self.ip)

	class Meta:
		ordering = ["-id"] 
