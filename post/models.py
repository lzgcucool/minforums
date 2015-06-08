#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: minforums/models.py

#from django.db import models
from mongoengine import *
from datetime import datetime
from bson import ObjectId

keyThread = '000000000000000000000000'

class Thread(Document):
	user_id = ObjectIdField(required=True)
	thread_id = ObjectIdField(default=ObjectId(keyThread))
	title = StringField(max_length=100)
	click = IntField()
	postime = DateTimeField(default=datetime.now(), required=True)
	lastdate = DateTimeField()
	content = StringField()
	meta = {'ordering':['-postime']}
