#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: accounts/urls.py

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'minforums.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^login/$', 'accounts.views.login'),
    url(r'^logout/$', 'accounts.views.logout'),
    url(r'^register/$', 'accounts.views.register'),
    url(r'^forgotpassword/$', 'accounts.views.forgotpassword'),
    url(r'^setpassword/$', 'accounts.views.setpassword'),
)
