from django.conf.urls import url

from gtfsapp.views import FeedList, FeedInfoList, FeedAgencyList, FeedRouteList, FeedStopList, FeedServiceList, FeedShapeList, FeedFareList, FeedZoneList
from gtfsapp.views import FeedDetail, FeedInfoDetail, AgencyDetail, RouteDetail, StopDetail, ServiceDetail, ShapeDetail, FareDetail, ZoneDetail

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
    url(r'feed/(?P<feed_id>\d+)/stop/(?P<pk>\d+)/$', StopDetail.as_view(), name='stop_detail'),
    url(r'feed/(?P<feed_id>\d+)/service/(?P<pk>\d+)/$', ServiceDetail.as_view(), name='service_detail'),
    url(r'feed/(?P<feed_id>\d+)/shape/(?P<pk>\d+)/$', ShapeDetail.as_view(), name='shape_detail'),
    url(r'feed/(?P<feed_id>\d+)/fare/(?P<pk>\d+)/$', FareDetail.as_view(), name='fare_detail'),
    url(r'feed/(?P<feed_id>\d+)/zone/(?P<pk>\d+)/$', ZoneDetail.as_view(), name='zone_detail'),

]
