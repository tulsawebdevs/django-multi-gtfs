#
# Copyright 2012-2014 John Whitlock
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import unicode_literals

from django.contrib.gis import admin

from multigtfs.app_settings import MULTIGTFS_OSMADMIN
from multigtfs.models import (
    Agency, Block, Fare, FareRule, Feed, FeedInfo, Frequency, Route, Service,
    ServiceDate, Shape, ShapePoint, Stop, StopTime, Transfer, Trip, Zone)

geo_admin = admin.OSMGeoAdmin if MULTIGTFS_OSMADMIN else admin.GeoModelAdmin


admin.site.register(Agency)
admin.site.register(Block)
admin.site.register(Fare)
admin.site.register(FareRule)
admin.site.register(Feed)
admin.site.register(FeedInfo)
admin.site.register(Frequency)
admin.site.register(Route, geo_admin)
admin.site.register(Service)
admin.site.register(ServiceDate)
admin.site.register(Shape, geo_admin)
admin.site.register(ShapePoint, geo_admin)
admin.site.register(Stop, geo_admin)
admin.site.register(StopTime)
admin.site.register(Transfer)
admin.site.register(Trip, geo_admin)
admin.site.register(Zone)
