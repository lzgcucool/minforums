#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: accounts/urls.py

from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'minforums.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'minforums.views.showhomepage', name="homepage"),
    url(r'^(?P<page>[0-9]+)$', 'minforums.views.showhomepage', name="homepaging"),
    url(r'^profile-(?P<names>[0-9A-Za-z]+)/(?P<page>[0-9]+)$', 'minforums.views.showhomepage', name="userhomepaging"),
    url(r'^thread/(?P<tmid>[0-9A-Za-z]+)/', 'minforums.views.showthread', name="showthread"),
    url(r'^member/', 'minforums.views.userpage', name="userpage"),
    url(r'^account/', include('accounts.urls')),
    url(r'^post/', include('post.urls')),
    #url(r'^admin/', include(admin.site.urls)),
)
