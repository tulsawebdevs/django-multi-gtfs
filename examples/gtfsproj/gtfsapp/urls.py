from django.conf.urls import url, include

from gtfsapp.views import (
    FeedList, FeedInfoList, FeedAgencyList, FeedRouteList, 
    FeedStopList, FeedServiceList, FeedShapeList, FeedFareList, 
    FeedZoneList, 

    FeedDetail, FeedInfoDetail, AgencyDetail, 
    RouteDetail, TripDetail, StopDetail, StopTimeDetail, 
    ServiceDetail, ShapeDetail, ShapePointDetail, FareDetail, 
    ZoneDetail, 

    StopTimeByStopList, FareRuleByRouteList, TripByRouteList,

    FrequencyByTripList, StopTimeByTripList, 

    TripByShapeList, ShapePointByShapeList,

)

urlpatterns = [
    url(r'^$', FeedList.as_view(), name='feed_list'),
    url(r'feed/(?P<feed_id>\d+)/feedinfo/$', FeedInfoList.as_view(), name='feedinfo_list'),
    url(r'feed/(?P<feed_id>\d+)/agency/$', FeedAgencyList.as_view(), name='agency_list'),
    url(r'feed/(?P<feed_id>\d+)/route/$', FeedRouteList.as_view(), name='route_list'),
    url(r'feed/(?P<feed_id>\d+)/stop/$', FeedStopList.as_view(), name='stop_list'),
    url(r'feed/(?P<feed_id>\d+)/service/$', FeedServiceList.as_view(), name='service_list'),
    url(r'feed/(?P<feed_id>\d+)/shape/$', FeedShapeList.as_view(), name='shape_list'),
    url(r'feed/(?P<feed_id>\d+)/fare/$', FeedFareList.as_view(), name='fare_list'),
    url(r'feed/(?P<feed_id>\d+)/zone/$', FeedZoneList.as_view(), name='zone_list'),

    url(r'^feed/(?P<pk>\d+)/$', FeedDetail.as_view(), name='feed_detail'),
    url(r'feed/(?P<feed_id>\d+)/feedinfo/(?P<pk>\d+)/$', FeedInfoDetail.as_view(), name='feedinfo_detail'),
    url(r'feed/(?P<feed_id>\d+)/agency/(?P<pk>\d+)/$', AgencyDetail.as_view(), name='agency_detail'),
    url(r'feed/(?P<feed_id>\d+)/route/(?P<pk>\d+)/$', RouteDetail.as_view(), name='route_detail'),
    url(r'feed/(?P<feed_id>\d+)/trip/(?P<pk>\d+)/$', TripDetail.as_view(), name='trip_detail'),
    url(r'feed/(?P<feed_id>\d+)/stop/(?P<pk>\d+)/$', StopDetail.as_view(), name='stop_detail'),
    url(r'feed/(?P<feed_id>\d+)/stoptime/(?P<pk>\d+)/$', StopTimeDetail.as_view(), name='stoptime_detail'),
    url(r'feed/(?P<feed_id>\d+)/service/(?P<pk>\d+)/$', ServiceDetail.as_view(), name='service_detail'),
    url(r'feed/(?P<feed_id>\d+)/shape/(?P<pk>\d+)/$', ShapeDetail.as_view(), name='shape_detail'),
    url(r'feed/(?P<feed_id>\d+)/shapepoint/(?P<pk>\d+)$', ShapePointDetail.as_view(), name='shapepoint_detail'),

    url(r'feed/(?P<feed_id>\d+)/fare/(?P<pk>\d+)/$', FareDetail.as_view(), name='fare_detail'),
    url(r'feed/(?P<feed_id>\d+)/zone/(?P<pk>\d+)/$', ZoneDetail.as_view(), name='zone_detail'),

    url(r'feed/(?P<feed_id>\d+)/route/(?P<route_id>\d+)/farerule/$', FareRuleByRouteList.as_view(), name='farerule_by_route_list'),
    url(r'feed/(?P<feed_id>\d+)/route/(?P<route_id>\d+)/trip/$', TripByRouteList.as_view(), name='trip_by_route_list'),

    url(r'feed/(?P<feed_id>\d+)/trip/(?P<trip_id>\d+)/frequency/$', FrequencyByTripList.as_view(), name='frequency_by_trip_list'),
    url(r'feed/(?P<feed_id>\d+)/trip/(?P<trip_id>\d+)/stoptime/$', StopTimeByTripList.as_view(), name='stoptime_by_trip_list'),

    url(r'feed/(?P<feed_id>\d+)/stop/(?P<stop_id>\d+)/stoptime/$', StopTimeByStopList.as_view(), name='stoptime_by_stop_list'),


    url(r'feed/(?P<feed_id>\d+)/shape/(?P<shape_id>\d+)/shapepoint/$', ShapePointByShapeList.as_view(), name='shapepoint_by_shape_list'),
    url(r'feed/(?P<feed_id>\d+)/shape/(?P<shape_id>\d+)/trip/$', TripByShapeList.as_view(), name='trip_by_shape_list'),

]
