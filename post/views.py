#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: post/views.py

#from django.shortcuts import render
from django.http import HttpResponse
from accounts.models import User, _checklogin, _is_user, _user_verify
from post.models import Thread
from datetime import datetime
from json import dumps
from bson import ObjectId

def writethread(request):
	if request.method =='POST' and _is_user:
		title = request.POST['title']
		post = Thread.objects(title=title)
		# try:
		# 	post = Thread.objects(title=title)
		# except Thread.DoesNotExist:
		# 	return HttpResponse(u'failed')
		# if post:
		# 	return HttpResponse(u'failed')
		postobj = Thread(title=title)
		postobj.user_id = ObjectId(request.POST['user_id'])
		# if request.POST['thread_id']:
		postobj.thread_id = ObjectId(request.POST['thread_id'])
		postobj.content = request.POST['content']
		postobj.save()
		repost = dumps({'title':postobj.title,'id':str(postobj.id)}, ensure_ascii=False, indent=2)
		return HttpResponse(repost)
	else:
		return HttpResponse(u'failed')

def editthread(request):
	if request.method =='POST' and _is_user:
		thid = request.POST['id']
		try:
			post = Thread.objects(id=thid)
		except Thread.DoesNotExist:
			return HttpResponse(u'failed')
		post.title = request.POST['title']
		post.content = request.POST['content']
		post.lastdate = datetime.now()
		post.update()
		return HttpResponse(u'succeed')
	else:
		return HttpResponse(u'failed')

def delthread(request):
	if request.method =='POST' and _is_user:
		thid = request.POST['id']
		try:
			post = Thread.objects(id=thid)
		except Thread.DoesNotExist:
			return HttpResponse(u'failed')
		post.delete()
		return HttpResponse(u'succeed')
	else:
		return HttpResponse(u'failed')
