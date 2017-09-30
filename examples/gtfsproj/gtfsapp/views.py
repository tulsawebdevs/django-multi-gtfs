# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView, DetailView

from multigtfs.models import Feed, FeedInfo, Agency, Route, Service, Stop, Shape, Fare, Zone

# List feed
class FeedList(ListView):
    queryset = Feed.objects.order_by('name', '-created')

# Filter lists by feed
class ByFeedListView(ListView):
    by_col = 'feed_id'
    by_kwarg = 'feed_id'
    by_class = Feed
    by_classname = 'feed'

    def get_context_data(self, **kwargs):
        context = super(ByFeedListView, self).get_context_data(
            **kwargs)
        context[self.by_classname] = self.by_class.objects.get(
            id=self.kwargs[self.by_kwarg])
        context['feed_id'] = self.kwargs['feed_id']
        return context

    def get_queryset(self, **kwargs):
        q_filter = {self.by_col: self.kwargs[self.by_kwarg]}
        qset = super(ByFeedListView, self).get_queryset(**kwargs)
        return qset.filter(**q_filter)


# List
class FeedInfoList(ByFeedListView):
    model = FeedInfo

class FeedAgencyList(ByFeedListView):
    model = Agency

class FeedStopList(ByFeedListView):
    model = Stop

class FeedRouteList(ByFeedListView):
    model = Route

class  FeedShapeList(ByFeedListView):
    model = Shape

class FeedServiceList(ByFeedListView):
    model = Service

class FeedZoneList(ByFeedListView):
    model = Zone

class FeedFareList(ByFeedListView):
    model = Fare


# Detail
class FeedDetail(DetailView):
    model = Feed

class FeedInfoDetail(DetailView):
    model = FeedInfo

class AgencyDetail(DetailView):
    model = Agency

class StopDetail(DetailView):
    model = Stop

class RouteDetail(DetailView):
    model = Route

class ShapeDetail(DetailView):
    model = Shape

class ServiceDetail(DetailView):
    model = Service

class ZoneDetail(DetailView):
    model = Zone

class FareDetail(DetailView):
    model = Fare

