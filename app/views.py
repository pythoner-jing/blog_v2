# Create your views here.
#coding:utf-8

from django.http import HttpResponse
from django.shortcuts import render_to_response, RequestContext, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test 

from models import *

import random
import urllib

def distribute_add_link(distributes):
	dd = distributes
	for d in dd:
		d.read = "/read/" + urllib.quote(d.title.encode("utf-8")) + "/"
		d.edit = "/edit/" + urllib.quote(d.title.encode("utf-8")) + "/"
		d.delete = "/delete/" + urllib.quote(d.title.encode("utf-8")) + "/"
	return dd

def tag_add_link(tags):
	tt = tags
	for t in tt:
		t.url = "/tag/" + urllib.quote(t.tagname.encode("utf-8")) + "/"
	return tt

def index(request):
	tags = Tag.objects.all()
	tags = tag_add_link(tags)
	activitys = Activity.objects.all()
	mottos = Motto.objects.all()
	motto = random.choice(mottos)
	distributes = Distribute.objects.all()
	distributes = distribute_add_link(distributes)

	return render_to_response("index.html", {"user" : request.user, "tags" : tags, "activitys" : activitys, "distributes" : distributes, "motto" : motto})

def read(request, title):
	tags = Tag.objects.all()
	tags = tag_add_link(tags)
	activitys = Activity.objects.all()
	mottos = Motto.objects.all()
	motto = random.choice(mottos)

	title = urllib.unquote(title.encode("utf-8"))

	distribute = Distribute.objects.get(title = title)

	return render_to_response("read.html", {"tags" : tags, "activitys" : activitys, "distribute" : distribute, "motto" : motto})

def test_login(user):
	return user.is_authenticated() and user.is_active

@user_passes_test(test_login, login_url = "/login/")
def distribute(request):
	tags = Tag.objects.all()
	tags = tag_add_link(tags)
	activitys = Activity.objects.all()
	mottos = Motto.objects.all()
	motto = random.choice(mottos)

	if request.method == "POST":
		title = request.POST.get("title", "").strip()
		#重复标题
		if Distribute.objects.filter(title = title):
			return HttpResponseRedirect("/")
		distribute = Distribute(title = title, counter = 0)
		distribute.save()

		user = User.objects.get(username = "JING")
		activity = Activity.objects.create(user = user, action = "发布", distribute = distribute)
		activity.save()

		return HttpResponseRedirect("/")

	return render_to_response("distribute.html", {"tags" : tags, "activitys" : activitys, "motto" : motto}, context_instance = RequestContext(request)) 

@user_passes_test(test_login, login_url = "/login/")
def edit(request, title):
	tags = Tag.objects.all()
	tags = tag_add_link(tags)
	activitys = Activity.objects.all()
	mottos = Motto.objects.all()
	motto = random.choice(mottos)
	title = urllib.unquote(title.encode("utf-8"))
	distribute = Distribute.objects.get(title = title)
	distribute.taglist = [t.tagname for t in distribute.tags.all()]

	if request.method == "POST":
		blog_tags = request.POST.getlist("tag") 
		for t in tags:
			if t.tagname in blog_tags:
				try:
					p, created = Tag.objects.get_or_create(tagname = t.tagname)
					distribute.tags.add(p)
				except Exception, e:
					print "add异常", e
			else:
				try:
					p, created = Tag.objects.get_or_create(tagname = t.tagname)
					distribute.tags.remove(p)
				except Exception, e:
					print "remove异常", e
		content = request.POST.get("editbox", "") 
		distribute.content = content
		distribute.save()

		return HttpResponseRedirect("")

	return render_to_response("edit.html", {"tags" : tags, "activitys" : activitys, "motto" : motto, "distribute" : distribute}, context_instance = RequestContext(request)) 

@user_passes_test(test_login, login_url = "/login/")
def delete(request, title):
	tags = Tag.objects.all()
	tags = tag_add_link(tags)
	activitys = Activity.objects.all()
	mottos = Motto.objects.all()
	motto = random.choice(mottos)

	if request.method == "POST":
		password = request.POST.get("password", "").strip()
		user = auth.authenticate(username = request.user.username, password = password)
		if user is not None and user.is_active:
			title = urllib.unquote(title.encode("utf-8"))
			distribute = Distribute.objects.get(title = title)
			distribute.delete()
			return HttpResponseRedirect("/")
		else:
			return render_to_response("error.html", {"err_msg" : "密码错误", "user" : request.user, "tags" : tags, "activitys" : activitys, "motto" : motto}, context_instance = RequestContext(request))

	return render_to_response("delete.html", {"user" : request.user, "tags" : tags, "activitys" : activitys, "motto" : motto}, context_instance = RequestContext(request))

def error(request):
	tags = Tag.objects.all()
	tags = tag_add_link(tags)
	activitys = Activity.objects.all()
	mottos = Motto.objects.all()
	motto = random.choice(mottos)

	return render_to_response("error.html", {"err_msg" : "错误信息测试", "user" : request.user, "tags" : tags, "activitys" : activitys, "motto" : motto})

def login(request):
	tags = Tag.objects.all()
	tags = tag_add_link(tags)
	activitys = Activity.objects.all()
	mottos = Motto.objects.all()
	motto = random.choice(mottos)

	if request.method == "POST":
		username = request.POST.get("username", "").strip()
		password = request.POST.get("password", "").strip()
		user = auth.authenticate(username = username, password = password)
		if user is not None and user.is_active:
			auth.login(request, user)
			return HttpResponseRedirect("/")
		else:
			return render_to_response("error.html", {"err_msg" : "帐号或密码错误", "user" : request.user, "tags" : tags, "activitys" : activitys, "motto" : motto}, context_instance = RequestContext(request))
	return render_to_response("login.html", {"user" : request.user, "tags" : tags, "activitys" : activitys, "motto" : motto}, context_instance = RequestContext(request))

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/")

def tag(request, tagname):
	tags = Tag.objects.all()
	tags = tag_add_link(tags)
	activitys = Activity.objects.all()
	mottos = Motto.objects.all()
	motto = random.choice(mottos)

	tagname = urllib.unquote(tagname)
	distributes = [d for d in Distribute.objects.all() for t in d.tags.all() if t.tagname == tagname]
	distributes = list(set(distributes))
	distributes = distribute_add_link(distributes)

	return render_to_response("tag.html", {"title" : tagname, "user" : request.user, "tags" : tags, "activitys" : activitys, "motto" : motto, "distributes" : distributes})

def record(request, year, month):
	tags = Tag.objects.all()
	tags = tag_add_link(tags)
	activitys = Activity.objects.all()
	mottos = Motto.objects.all()
	motto = random.choice(mottos)

	return render_to_response("login.html", {"user" : request.user, "tags" : tags, "activitys" : activitys, "motto" : motto}, context_instance = RequestContext(request))
