#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: minforums/views.py

from django.shortcuts import render
# from accounts.models import _checklogin, _is_user
from post.models import Thread, keyThread
import accounts.models
from bson import ObjectId
from markdown import markdown

def showhomepage(request, **kargs):
	if kargs:
		if kargs.get('page'):
			page = int(kargs['page'])
		else:
			page = 1
		if kargs.get('names'):
			try:
				upages = accounts.models.User.objects.get(username=kargs['names'])
				upages = upages.id
			except accounts.models.User.DoesNotExist:
				upages = []
		else:
			upages = []
	else:
		page = 1
		upages = []
	first = (page-1)*10
	allnum = Thread.objects().count()
	page_count,tail = divmod(allnum,10)
	if tail is not 0:
		page_count+1
	if upages:
		post = Thread.objects(user_id=upages,thread_id=ObjectId(keyThread)).all()[first:10*page]
	else:
		post = Thread.objects(thread_id=ObjectId(keyThread)).all()[first:10*page]
	user = accounts.models._is_user(request)
	return render(request, 'home.html', locals())

def showthread(request,tmid):
	user = accounts.models._is_user(request)
	try:
		post = Thread.objects.get(id=ObjectId(tmid),thread_id=ObjectId(keyThread))
	except Thread.DoesNotExist:
		return HttpResponse('404')
	post.content = markdown(post.content)
	try:
		commit = Thread.objects(thread_id=post.id)
	except Thread.DoesNotExist:
		commit = []
	if commit:
		for i in range(len(commit)):
			com_user = accounts.models.User.objects.get(id=commit[i].user_id)
			commit[i].append(com_user.username)
			commit[i].email = com_user.emailadd
	if post.user_id == user.id:
		author = user
		author_self = True
	else:
		author = accounts.models.User.objects.get(id=post.user_id)
		author_self = False
	return render(request, 'thread.html', locals())

def userpage(request):
	user = accounts.models._is_user(request)
	users = accounts.models.User.objects()[0:50]
	return render(request, 'userpage.html', locals())