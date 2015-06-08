#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: accounts/views.py
from django.shortcuts import render
from accounts.models import User, _checklogin, _is_user
from minforums.settings import SECRET_KEY
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives
# from mongoengine import Q
from hashlib import md5
from random import sample
from datetime import datetime
import string

def login(request):
	if request.method =='POST':
		login_pass = True
		email = request.POST['email']
		try:
			userobj = User.objects.get(emailadd=email)
		except User.DoseNotExist:
			userobj = []
		if userobj is None:
			login_pass = False
		passwd = md5(SECRET_KEY+request.POST['password']+SECRET_KEY).hexdigest()
		if userobj.password != passwd:
			login_pass = False
		if login_pass == False:
			return HttpResponse(u'failed')
		else:
			userid = str(userobj.id)
			response = HttpResponse(u'succeed')
			response.set_cookie('verify',userid)
			response.set_cookie('safekey',md5(userid+SECRET_KEY+passwd).hexdigest())
			userobj.lastlogin = datetime.now()
			userobj.save()
			return response
	else:
		return HttpResponse('404')


def register(request):
	if request.method =='POST':
		reg_pass = True
		email = request.POST['email']
		user = request.POST['username']
		userobju = User.objects(emailadd=email)
		if not userobju:
			userobj = User.objects(username=user)
			if not userobj:
				users = User(username=user)
				users.emailadd = email
				users.profile = request.POST['profile']
				users.password = md5(SECRET_KEY+request.POST['password']+SECRET_KEY).hexdigest()
				users.save()
			else:
				reg_pass = False
		else:
			reg_pass = False
		if reg_pass:
			return HttpResponse(u'succeed')
		else:
			return HttpResponse(u'failed')

@_checklogin
def setpassword(request):
	if request.method =='POST':
		user_id = request.COOKIES["verify"]
		try:
			userobj = User.objects.get(id=user_id)
		except User.DoseNotExist:
			return HttpResponse(u'failed')
		if request.COOKIES["password"] == request.COOKIES["repassword"]:
			password = md5(SECRET_KEY+request.POST['password']+SECRET_KEY).hexdigest()
			userobj.password = password
			userobj.save()
			return HttpResponse(u'succeed')

	return render(request, 'setpassword.html', locals())

def forgotpassword(request):
	if request.method =='POST':
		email = request.POST['email']
		user = request.POST['username']
		try:
			userobju = User.objects.get(emailadd=email)
		except User.DoseNotExist:
			return HttpResponse(u'failed')
		if user != userobju.username:
			return HttpResponse(u'failed')
		source = ['9','8','7','6','5','4','3','2','1','0','z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a']
		source_str = string.join(sample(source,7)).replace(' ','')
		passwd = md5(SECRET_KEY+source_str+SECRET_KEY).hexdigest()
		userobju.password = passwd
		userobju.save()
		subject, from_email, to = u'重置密码邮件 - minforums', 'from@example.com', email
		text_content = u'密码已被重置:'+source_str
		html_content = u'<p>密码已被重置为：<strong>'+source_str+'</strong>,请尽快登陆系统修改.</p>'
		msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
		msg.attach_alternative(html_content, "text/html")
		msg.send()
	return HttpResponse(u'forgotpassword')

# @_checklogin
def logout(request):
	output = HttpResponse(u'logout')
	output.delete_cookie('verify', path='/')
	output.delete_cookie('safekey', path='/')
	# HttpResponseRedirect('/')
	return output