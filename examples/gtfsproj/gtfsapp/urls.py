from django.conf.urls import url

from gtfsapp.views import FeedList, FeedDetail

urlpatterns = [
    url(r'^$', FeedList.as_view(), name='feed_list'),
    url(r'^feed/(?P<pk>\d+)/$', FeedDetail.as_view(), name='feed_detail'),
]
