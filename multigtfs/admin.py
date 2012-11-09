#
# Copyright 2012 John Whitlock
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

from django.contrib import admin

from multigtfs.models import (
    Agency, Block, Fare, FareRule, Feed, FeedInfo, Frequency, Route, Service,
    ServiceDate, Shape, ShapePoint, Stop, StopTime, Transfer, Trip, Zone)

admin.site.register(Agency)
admin.site.register(Block)
admin.site.register(Fare)
admin.site.register(FareRule)
admin.site.register(Feed)
admin.site.register(FeedInfo)
admin.site.register(Frequency)
admin.site.register(Route)
admin.site.register(Service)
admin.site.register(ServiceDate)
admin.site.register(Shape)
admin.site.register(ShapePoint)
admin.site.register(Stop)
admin.site.register(StopTime)
admin.site.register(Transfer)
admin.site.register(Trip)
admin.site.register(Zone)
