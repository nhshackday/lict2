# -*- coding: UTF-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals
from django.conf.urls import patterns, url
from django.shortcuts import redirect
from .views import DoctorListView, StudyListView
from .views import RootRedirect

urlpatterns = patterns('conflict.views',
    url(r'^doctors/$', DoctorListView.as_view()),
    url(r'^studies/$', StudyListView.as_view()),
    url(r'^$', RootRedirect.as_view()),
)
