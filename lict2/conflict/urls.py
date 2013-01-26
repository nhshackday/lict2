# -*- coding: UTF-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals
from django.conf.urls import patterns, url
from .views import DoctorListView

urlpatterns = patterns('conflict.views',
    url(r'doctors/$', DoctorListView.as_view()),
)