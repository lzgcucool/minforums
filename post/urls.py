#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: accounts/urls.py

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'minforums.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^writethread/$', 'post.views.writethread'),
    url(r'^editthread/$', 'post.views.writethread'),
    url(r'^delthread/$', 'post.views.delthread'),
)
