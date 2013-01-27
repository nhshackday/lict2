# -*- coding: UTF-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals
from django.conf.urls import patterns, url
from django.shortcuts import redirect
from .views import DoctorListView
from .views import RootRedirect

urlpatterns = patterns('conflict.views',
    url(r'^doctors/$', DoctorListView.as_view()),
    url(r'^doctors/(?P<page>[0-9]+)/$', DoctorListView.as_view()),
    url(r'^$', RootRedirect.as_view()),
)
