from django.views.generic import ListView
from multigtfs.models import (
    Block, Fare, FareRule, Feed, Frequency, Route, Service, ServiceDate, Shape,
    ShapePoint, Stop, StopTime, Trip)


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


class FareRuleByFareListView(ListView):
    model = FareRule

    def get_context_data(self, **kwargs):
        context = super(FareRuleByFareListView, self).get_context_data(
            **kwargs)
        context['fare'] = Fare.objects.get(id=self.kwargs['fare_id'])
        context['feed_id'] = self.kwargs['feed_id']
        return context

    def get_queryset(self, **kwargs):
        return FareRule.objects.filter(fare_id=self.kwargs['fare_id'])


class FareRuleByRouteListView(ListView):
    model = FareRule

    def get_context_data(self, **kwargs):
        context = super(FareRuleByRouteListView, self).get_context_data(
            **kwargs)
        context['route'] = Route.objects.get(id=self.kwargs['route_id'])
        context['feed_id'] = self.kwargs['feed_id']
        return context

    def get_queryset(self, **kwargs):
        return FareRule.objects.filter(route_id=self.kwargs['route_id'])


class FrequencyByTripListView(ListView):
    model = Frequency

    def get_context_data(self, **kwargs):
        context = super(FrequencyByTripListView, self).get_context_data(
            **kwargs)
        context['trip'] = Trip.objects.get(id=self.kwargs['trip_id'])
        return context

    def get_queryset(self, **kwargs):
        return Frequency.objects.filter(trip=self.kwargs['trip_id'])


class ServiceDateByServiceListView(ListView):
    model = ServiceDate

    def get_context_data(self, **kwargs):
        context = super(ServiceDateByServiceListView, self).get_context_data(
            **kwargs)
        context['service'] = Service.objects.get(id=self.kwargs['service_id'])
        return context

    def get_queryset(self, **kwargs):
        return ServiceDate.objects.filter(service=self.kwargs['service_id'])


class ShapePointByShapeListView(ListView):
    model = ShapePoint

    def get_context_data(self, **kwargs):
        context = super(ShapePointByShapeListView, self).get_context_data(
            **kwargs)
        context['shape'] = Shape.objects.get(id=self.kwargs['shape_id'])
        context['feed_id'] = self.kwargs['feed_id']
        return context

    def get_queryset(self, **kwargs):
        return ShapePoint.objects.filter(shape=self.kwargs['shape_id'])


class StopTimeByStopListView(ListView):
    model = StopTime

    def get_context_data(self, **kwargs):
        context = super(StopTimeByStopListView, self).get_context_data(
            **kwargs)
        context['stop'] = Stop.objects.get(id=self.kwargs['stop_id'])
        context['feed_id'] = self.kwargs['feed_id']
        return context

    def get_queryset(self, **kwargs):
        return StopTime.objects.filter(stop_id=self.kwargs['stop_id'])


class StopTimeByTripListView(ListView):
    model = StopTime

    def get_context_data(self, **kwargs):
        context = super(StopTimeByTripListView, self).get_context_data(
            **kwargs)
        context['trip'] = Trip.objects.get(id=self.kwargs['trip_id'])
        context['feed_id'] = self.kwargs['feed_id']
        return context

    def get_queryset(self, **kwargs):
        return StopTime.objects.filter(trip=self.kwargs['trip_id'])


class TripByBlockListView(ListView):
    model = Trip

    def get_context_data(self, **kwargs):
        context = super(TripByBlockListView, self).get_context_data(**kwargs)
        context['the_block'] = Block.objects.get(id=self.kwargs['block_id'])
        context['feed_id'] = self.kwargs['feed_id']
        return context

    def get_queryset(self, **kwargs):
        return Trip.objects.filter(block_id=self.kwargs['block_id'])


class TripByRouteListView(ListView):
    model = Trip

    def get_context_data(self, **kwargs):
        context = super(TripByRouteListView, self).get_context_data(**kwargs)
        context['route'] = Route.objects.get(id=self.kwargs['route_id'])
        context['feed_id'] = self.kwargs['feed_id']
        return context

    def get_queryset(self, **kwargs):
        return Trip.objects.filter(route_id=self.kwargs['route_id'])


class TripByServiceListView(ListView):
    model = Trip

    def get_context_data(self, **kwargs):
        context = super(TripByServiceListView, self).get_context_data(**kwargs)
        context['service'] = Service.objects.get(id=self.kwargs['service_id'])
        context['feed_id'] = self.kwargs['feed_id']
        return context

    def get_queryset(self, **kwargs):
        return Trip.objects.filter(service=self.kwargs['service_id'])


class TripByShapeListView(ListView):
    model = ShapePoint

    def get_context_data(self, **kwargs):
        context = super(TripByShapeListView, self).get_context_data(**kwargs)
        context['shape'] = Shape.objects.get(id=self.kwargs['shape_id'])
        context['feed_id'] = self.kwargs['feed_id']
        return context

    def get_queryset(self, **kwargs):
        return Trip.objects.filter(shape=self.kwargs['shape_id'])
