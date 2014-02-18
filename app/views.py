# Create your views here.
#coding:utf-8

from django.http import HttpResponse
from django.shortcuts import render_to_response, RequestContext, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User

from models import *

import random

def index(request):
	tags = Tag.objects.all()
	activitys = Activity.objects.all()
	mottos = Motto.objects.all()
	distributes = Distribute.objects.all()

	motto = random.choice(mottos)

	return render_to_response("index.html", {"tags" : tags, "activitys" : activitys, "mottos" : mottos, "distributes" : distributes, "motto" : motto})
