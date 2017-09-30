# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.views.generic import ListView, DetailView
from multigtfs.models import Feed

class FeedList(ListView):
    #model = Feed
    queryset = Feed.objects.order_by('name', '-created')

class FeedDetail(DetailView):
    model = Feed
