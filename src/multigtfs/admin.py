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
