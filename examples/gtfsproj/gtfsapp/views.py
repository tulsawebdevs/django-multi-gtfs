# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView, DetailView

from multigtfs.models import (
    Feed, FeedInfo, Agency, Route, Trip, Service, Stop, 
    Shape, ShapePoint, Fare, Zone, StopTime, FareRule, Frequency
)

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


class StopTimeByStopList(ListView):
    model = StopTime

    def get_context_data(self, **kwargs):
        context = super(StopTimeByStopList, self).get_context_data(
            **kwargs)
        context['stop'] = Stop.objects.get(id=self.kwargs['stop_id'])
        context['feed_id'] = self.kwargs['feed_id']
        return context

    def get_queryset(self, **kwargs):
        return StopTime.objects.filter(stop_id=self.kwargs['stop_id'])


# Detail
class FeedDetail(DetailView):
    model = Feed

class FeedInfoDetail(DetailView):
    model = FeedInfo

class AgencyDetail(DetailView):
    model = Agency

class StopDetail(DetailView):
    model = Stop

class StopTimeDetail(DetailView):
    model = StopTime

class RouteDetail(DetailView):
    model = Route

class TripDetail(DetailView):
    model = Trip

class ShapeDetail(DetailView):
    model = Shape

class ShapePointDetail(DetailView):
    model = ShapePoint

class ServiceDetail(DetailView):
    model = Service

class ZoneDetail(DetailView):
    model = Zone

class FareDetail(DetailView):
    model = Fare


class TripByRouteList(ListView):
    model = Trip

    def get_context_data(self, **kwargs):
        context = super(TripByRouteList, self).get_context_data(**kwargs)
        context['route'] = Route.objects.get(id=self.kwargs['route_id'])
        context['feed_id'] = self.kwargs['feed_id']
        return context

    def get_queryset(self, **kwargs):
        return Trip.objects.filter(route_id=self.kwargs['route_id'])


class FareRuleByRouteList(ListView):
    model = FareRule

    def get_context_data(self, **kwargs):
        context = super(FareRuleByRouteList, self).get_context_data(
            **kwargs)
        context['route'] = Route.objects.get(id=self.kwargs['route_id'])
        context['feed_id'] = self.kwargs['feed_id']
        return context

    def get_queryset(self, **kwargs):
        return FareRule.objects.filter(route_id=self.kwargs['route_id'])


class StopTimeByTripList(ListView):
    model = StopTime

    def get_context_data(self, **kwargs):
        context = super(StopTimeByTripList, self).get_context_data(
            **kwargs)
        context['trip'] = Trip.objects.get(id=self.kwargs['trip_id'])
        context['feed_id'] = self.kwargs['feed_id']
        return context

    def get_queryset(self, **kwargs):
        return StopTime.objects.filter(trip=self.kwargs['trip_id'])


class FrequencyByTripList(ListView):
    model = Frequency

    def get_context_data(self, **kwargs):
        context = super(FrequencyByTripList, self).get_context_data(
            **kwargs)
        context['trip'] = Trip.objects.get(id=self.kwargs['trip_id'])
        context['feed_id'] = self.kwargs['feed_id']
        return context

    def get_queryset(self, **kwargs):
        return Frequency.objects.filter(trip=self.kwargs['trip_id'])



class TripByShapeList(ListView):
    model = ShapePoint

    def get_context_data(self, **kwargs):
        context = super(TripByShapeList, self).get_context_data(**kwargs)
        context['shape'] = Shape.objects.get(id=self.kwargs['shape_id'])
        context['feed_id'] = self.kwargs['feed_id']
        return context

    def get_queryset(self, **kwargs):
        return Trip.objects.filter(shape=self.kwargs['shape_id'])

class ShapePointByShapeList(ListView):
    model = ShapePoint

    def get_context_data(self, **kwargs):
        context = super(ShapePointByShapeList, self).get_context_data(
            **kwargs)
        context['shape'] = Shape.objects.get(id=self.kwargs['shape_id'])
        context['feed_id'] = self.kwargs['feed_id']
        return context

    def get_queryset(self, **kwargs):
        return ShapePoint.objects.filter(shape=self.kwargs['shape_id'])



