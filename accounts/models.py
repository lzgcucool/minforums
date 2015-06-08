#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: accounts/models.py

#from django.db import models
from mongoengine import *
from django.http import HttpResponseRedirect
from hashlib import md5
from datetime import datetime
from minforums.views import showhomepage
from minforums.settings import SECRET_KEY



def _user_verify(request):
	if request.COOKIES.get('verify') is not None:
		is_verify = request.COOKIES["verify"]
	else:
		is_verify = False
	return is_verify

def _is_user(request):
	is_pass = True
	user_verify_id = _user_verify(request)
	if user_verify_id:
		try:
			user = User.objects.get(id=user_verify_id)
		except User.DoesNotExist:
			return False
		userid = str(user.id)
		safekey = md5(userid+SECRET_KEY+user.password).hexdigest()
		if safekey == request.COOKIES.get('safekey'):
			is_pass = user
		else:
			is_pass = False
	else:
		is_pass = False
	return is_pass

def _checklogin(func):
	def _login(request):
		if _is_user(request):
			return showhomepage(request)
		else:
			return func(request)
	return _login


class User(Document):
	username = StringField(max_length=100, required=True)
	password = StringField(max_length=50, required=True)
	emailadd = EmailField(max_length=100, required=True)
	lastlogin = DateTimeField(default=datetime.now())
	profile = StringField(max_length=150)
	meta = {'ordering':['-lastlogin']}