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

from django.utils.html import format_html
from django.core.urlresolvers import reverse, NoReverseMatch
    
geo_admin = admin.OSMGeoAdmin if MULTIGTFS_OSMADMIN else admin.GeoModelAdmin


# Define inline lists
class InlineEditLink():

    def edit_link(self, instance):
        """
        Provide link to admin edit view, note 'edit_link' must be included in fields and
        readonly_fields in child class. 
        """
        url = reverse('admin:%s_%s_change' % (instance._meta.app_label, instance._meta.module_name),
                args=(instance.pk,))
        return (format_html(u'<a href="{}">Edit</a>', url) if instance.pk is not None else '')
    edit_link.short_description = ''

        
class FeedInfoInline(admin.StackedInline):
    model = FeedInfo
    fields = ('publisher_name', 'publisher_url', 'start_date', 'end_date', 'version', 'lang', 'extra_data', )
    extra = 0

    
class AgencyInline(admin.TabularInline, InlineEditLink):
    model = Agency
    fields = ('edit_link', 'agency_id', 'name', 'url', 'timezone')
    readonly_fields = ('edit_link', )
    extra = 0
 
class ZoneInline(admin.TabularInline, InlineEditLink):
    model = Zone
    fields = ('edit_link', 'feed', 'zone_id', )
    readonly_fields = ('edit_link', )
    extra = 0

    
class FareInline(admin.TabularInline, InlineEditLink):        
    model = Fare
    fields = ('edit_link', 'feed', 'fare_id', 'price', 'payment_method', 'transfers', 'transfer_duration', 'currency_type', )
    readonly_fields = ('edit_link', )
    extra = 0

    
class RouteInline(admin.TabularInline, InlineEditLink):
    model = Route
    fields = ('edit_link', 'short_name', 'long_name', 'desc', 'rtype', 'feed', 'agency')
    readonly_fields = ['edit_link', 'short_name', 'long_name', 'desc', 'rtype', 'feed', 'agency']
    
    extra = 0
    def has_add_permission(self, request):
        """Disable add another record option"""
        return False  


class ServiceDateInline(admin.TabularInline):
    model = ServiceDate
    fields = ('service','date','exception_type')

    extra = 0
    def has_add_permission(self, request):
        """Disable add another record option"""
        return False 


class TripInline(admin.TabularInline, InlineEditLink):
    model = Trip
    fields = ('edit_link', 'route', 'service', 'headsign', 'short_name', 'direction', 'block', 'wheelchair_accessible', 'bikes_allowed')
    readonly_fields = ['edit_link', 'route', 'service', 'headsign', 'short_name', 'direction', 'block', 'wheelchair_accessible', 'bikes_allowed']

    extra = 0
    def has_add_permission(self, request):
        """Disable add another record option"""
        return False    


class StopTimeInline(admin.TabularInline, InlineEditLink):
    model = StopTime
    fields = ('edit_link', 'stop', 'arrival_time', 'departure_time', 'stop_headsign', 
        'pickup_type', 'drop_off_type', 'shape_dist_traveled')
    readonly_fields = ['edit_link', 'stop', 'arrival_time', 'departure_time', 'stop_headsign', 
        'pickup_type', 'drop_off_type', 'shape_dist_traveled']

    extra = 0
    def has_add_permission(self, request):
        """Disable add another record option"""
        return False    


class FrequencyInline(admin.TabularInline):
    model = Frequency
    fields = ('trip', 'start_time', 'end_time', 'headway_secs', 'exact_times', )
    readonly_fields = ('trip', 'start_time', 'end_time', 'headway_secs', 'exact_times', )

    extra = 0
    def has_add_permission(self, request):
        """Disable add another record option"""
        return False  
        

class FareRuleInline(admin.TabularInline, InlineEditLink):
    model = FareRule
    fields = ('edit_link', 'fare', 'route', 'origin', 'destination', 'contains', )
    readonly_fields = ('edit_link', )
    extra = 0

    
class OriginZoneFareRuleInline(FareRuleInline):
    verbose_name = "Origin zone fare rule"
    verbose_name_plural = "Origin zone fare rules"
    fk_name  = 'origin'

    
class DestinationZoneFareRuleInline(FareRuleInline):
    verbose_name = "Destination zone fare rule"
    verbose_name_plural = "Destination zone fare rules"
    fk_name  = 'destination'
    

class StopTransferInline(admin.TabularInline, InlineEditLink):
    model = Transfer 
    fields = ('edit_link', 'from_stop', 'to_stop', 'transfer_type', 'min_transfer_time', )
    readonly_fields = ('edit_link', )
    extra = 0
    fk_name  = 'from_stop'


class FromStopTransferInline(StopTransferInline):
    verbose_name = "Transfer from stop"
    verbose_name_plural = "Transfers from stop"
    fk_name  = 'from_stop'

    
class ToStopTransferInline(StopTransferInline):
    verbose_name = "Transfer to stop"
    verbose_name_plural = "Transfers to stop"
    fk_name  = 'to_stop'

    
class ShapePointInline(admin.TabularInline, InlineEditLink):
    model = ShapePoint
    fields = ('edit_link', 'shape', 'sequence', 'traveled', 'point', )
    readonly_fields = ('edit_link', 'shape', 'sequence', 'traveled', 'point', )
    extra = 0

    
    
    
# Define admin pages
    
class FeedAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')
    list_display_links = ['name']
    
    inlines = [FeedInfoInline, ZoneInline, FareInline, AgencyInline]

    
class FareAdmin(admin.ModelAdmin):
    raw_id_fields = ('feed', )
    list_display = ('feed', 'fare_id', 'price', 'payment_method', 'transfers', 'transfer_duration', 'currency_type', 'extra_data', )
    list_display_links = ['fare_id']

    fieldsets = (
        (None, {
            'fields': ('feed', 'fare_id', ('price', 'currency_type', ), 'payment_method', ('transfers', 'transfer_duration', ), )
        }),
        ('Additional options', {
            'classes': ('collapse',),
            'fields': ('extra_data', )
        }), 
    )
    
    inlines = [FareRuleInline]

    
class ZoneAdmin(admin.ModelAdmin):
    raw_id_fields = ('feed', )
    list_display = ('feed', 'zone_id', )
    list_display_links = ['zone_id']
    
    inlines = [OriginZoneFareRuleInline, DestinationZoneFareRuleInline]
    
    
class AgencyAdmin(admin.ModelAdmin):
    raw_id_fields = ('feed', )
    list_display = ('agency_id', 'name', 'feed', 'url', 'timezone')
    list_display_links = ['name']
    list_filter = ['name', 'feed']
    
    fieldsets = (
        (None, {
            'fields': ('feed', ('name', 'agency_id', ), 'url', 'timezone', )
        }),
        ('Additional options', {
            'classes': ('collapse',),
            'fields': ('phone', 'fare_url', 'lang', 'extra_data')
        }),
    )
    
    inlines = [RouteInline]


class RouteAdmin(geo_admin):
    raw_id_fields = ('feed', 'agency')
    list_display = ('feed', 'agency', 'route_id', 'rtype', 'short_name', 'long_name')
    list_display_links = ['route_id']
    list_filter = ['feed', 'agency']
    
    fieldsets = (
        (None, {
            'fields': (('feed', 'agency', ), ('route_id', 'short_name', 'long_name', ),  'rtype', 'geometry', )
        }),
        ('Additional options', {
            'classes': ('collapse', ),
            'fields': ('url', 'color', 'text_color', 'desc', 'extra_data', )
        }), 
    )
    
    inlines = [TripInline, FareRuleInline]
    
    

class ServiceAdmin(admin.ModelAdmin):
    raw_id_fields = ('feed', )
    list_display = ('feed', 'service_id', 'monday', 'tuesday', 'wednesday', 
        'thursday', 'friday', 'saturday', 'sunday', 'start_date', 'end_date')
    list_display_links = ['service_id']
    list_filter = ['feed', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    fields = ('feed', 'service_id', ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',), ('start_date', 'end_date', ), )
    
    inlines = [TripInline, ServiceDateInline]

 
   
class BlockAdmin(admin.ModelAdmin):
    raw_id_fields = ('feed', )
    list_display = ('block_id', 'feed', )
    list_display_links = ('block_id', )

    inlines = [TripInline]

    

class StopAdmin(geo_admin):
    raw_id_fields = ('feed', 'zone', 'parent_station')
    list_display = ('feed', 'stop_id', 'code', 'name', 'location_type', 'wheelchair_boarding', 'parent_station', 'desc', 'zone', 'url')
    list_display_links = ['stop_id']
    list_filter = ['feed', 'location_type', 'zone', 'wheelchair_boarding']

    fieldsets = (
        (None, {
            'fields': ('feed', ('stop_id', 'code', 'name', ), ('location_type', 'wheelchair_boarding', ), 'point')
        }),
        ('Additional options', {
            'classes': ('collapse',),
            'fields': ('parent_station', 'desc', 'zone', 'url', 'extra_data')
        }), 
    )
 
    inlines = [StopTimeInline, FromStopTransferInline, ToStopTransferInline]

class TripAdmin(geo_admin):
    raw_id_fields = ('route', 'service', 'block', 'shape')
    list_display = ('route', 'trip_id', 'service', 'direction', 'headsign', 'short_name', 'block', 'wheelchair_accessible', 'bikes_allowed')
    list_display_links = ['trip_id']

    fieldsets = (
        (None, {
            'fields': ('trip_id', ('route', 'service', 'block', ), ('direction', 'headsign', ), ('shape', 'geometry', ), )
        }),
        ('Additional options', {
            'classes': ('collapse',),
            'fields': ('short_name', ('wheelchair_accessible', 'bikes_allowed', ), 'extra_data')
        }), 
    )
    
    inlines = [FrequencyInline, StopTimeInline]

    
class FrequencyAdmin(admin.ModelAdmin):
    raw_id_fields = ('trip', )
    list_display = ('trip', 'start_time', 'end_time', 'headway_secs', 'exact_times', )
    list_display_links = ['trip']

    fieldsets = (
        (None, {
            'fields': ('trip', 'start_time', 'end_time', 'headway_secs', 'exact_times', )
        }),
        ('Additional options', {
            'classes': ('collapse',),
            'fields': ('extra_data', )
        }), 
    )

    
class StopTimeAdmin(admin.ModelAdmin):
    raw_id_fields = ('stop', 'trip')
    list_display = ('trip', 'stop_sequence', 'stop', 'arrival_time', 'departure_time', 'stop_headsign', 
        'pickup_type', 'drop_off_type', 'shape_dist_traveled')
    list_display_links = ['stop_sequence']

    fieldsets = (
        (None, {
            'fields': ('trip', 'stop_sequence', 'stop', 'arrival_time', 'departure_time')
        }),
        ('Additional options', {
            'classes': ('collapse',),
            'fields': ('stop_headsign', 'pickup_type', 'drop_off_type', 'shape_dist_traveled')
        }), 
    )

    
   
class FareRuleAdmin(admin.ModelAdmin):
    raw_id_fields = ('fare', 'route', 'origin', 'destination', 'contains', )
    list_display = ('fare', 'route', 'origin', 'destination', 'contains', )
    
    fieldsets = (
        (None, {
            'fields': ('fare', 'route', 'origin', 'destination', 'contains', )
        }),
        ('Additional options', {
            'classes': ('collapse', ),
            'fields': ('extra_data', )
        }), 
    )
    
    
class TransferAdmin(admin.ModelAdmin):
    raw_id_fields = ('from_stop', 'to_stop')
    list_display = ('from_stop', 'to_stop', 'transfer_type', 'min_transfer_time', )
    
    fieldsets = (
        (None, {
            'fields': ('from_stop', 'to_stop', 'transfer_type', 'min_transfer_time', )
        }),
        ('Additional options', {
            'classes': ('collapse', ),
            'fields': ('extra_data', )
        }), 
    )
    
    
class ShapeAdmin(geo_admin):
    raw_id_fields = ('feed', )
    list_display = ('feed', 'shape_id', )
    list_display_links = ('shape_id', )
 
    fields = ('feed', ('shape_id', 'geometry', ), )
 
    # TODO: ShapePointInline does not appear to display but no errors. Check link
    inlines = [TripInline, ShapePointInline]

    
class ShapePointAdmin(geo_admin):
    raw_id_fields = ('shape', )
    list_display = ('shape', 'sequence', 'traveled', 'point', )
    list_display_links = ('point', )
 
    fieldsets = (
        (None, {
            'fields': ('shape', ('sequence', 'traveled', ), 'point', )
        }),
        ('Additional options', {
            'classes': ('collapse', ),
            'fields': ('extra_data', )
        }), 
    )


admin.site.register(Feed, FeedAdmin)
admin.site.register(Fare, FareAdmin)
admin.site.register(Zone, ZoneAdmin)
admin.site.register(Agency, AgencyAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Block, BlockAdmin)
admin.site.register(Stop, StopAdmin)
admin.site.register(Trip, TripAdmin)
admin.site.register(Frequency, FrequencyAdmin)
admin.site.register(StopTime, StopTimeAdmin)
admin.site.register(FareRule, FareRuleAdmin)
admin.site.register(Transfer, TransferAdmin)
admin.site.register(Shape, ShapeAdmin)
admin.site.register(ShapePoint, ShapePointAdmin)

