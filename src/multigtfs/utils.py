from collections import defaultdict
from csv import DictReader
from zipfile import ZipFile

from multigtfs.models import (
    Agency, Block, Calendar, CalendarDate, FareAttributes, FareRules, Feed,
    FeedInfo, Frequency, Route, Shape, Stop, StopTime, Transfer, Trip, Zone)

def import_gtfs(gtfs_file, feed):
    """Import a GTFS file as feed

    Keyword arguments:
    zip_file - A path or file-like object for the GTFS feed
    feed - The Feed to associate the GTFS data with

    Returns is a list of objects imported
    """
    z = ZipFile(gtfs_file, 'r')
    files = z.namelist()
    print files

    gtfs_order = (
        ('agency.txt', import_agency),
        ('stops.txt', import_stops),
        ('routes.txt', import_routes),
        ('trips.txt', import_trips),
        ('stop_times.txt', import_stop_times),
        ('calendar.txt', import_calendar),
        ('calendar_dates.txt', import_calendar_dates),
        ('fare_attributes.txt', import_fare_attributes),
        ('fare_rules.txt', import_fare_attributes),
        ('shapes.txt', import_shapes),
        ('frequencies.txt', import_frequencies),
        ('transfers.txt', import_transfers),
        ('feed_info.txt', import_feed_info),
    )

    gtfs_objects = []
    for table_name, importer in gtfs_order:
        for f in files:
            if f.endswith(table_name):
                table = z.open(f)
                importer(table, feed)
    return gtfs_objects


def import_agency(agency_file, feed):
    """Import agency.txt into Agency records for feed.

    Keyword arguments:
    agency_file -- A open agency.txt for reading
    feed -- the Feed to associate the records with
    """
    reader = DictReader(agency_file)
    name_map = dict(agency_url='url', agency_name='name',
                    agency_phone='phone', agency_fare_url='fare_url',
                    agency_timezone='timezone', agency_lang='lang')
    for row in reader:
        fields = dict((name_map.get(k, k), v) for k,v in row.items())
        Agency.objects.create(feed=feed, **fields)


def import_stops(stops_file, feed):
    """Import stops.txt into Stop records for feed

    Keyword arguments:
    stops_file -- A open stops.txt for reading
    feed -- the Feed to associate the records with

    Zone objects may also be created, if referenced in the stops
    """
    reader = DictReader(stops_file)
    parent_of = defaultdict(list)
    zones = defaultdict(list)
    name_map = dict(stop_code='code', stop_name='name', stop_desc='desc',
                    stop_lat='lat', stop_lon='lon', stop_url='url',
                    stop_timezone='timezone')
    for row in reader:
        fields = dict((name_map.get(k, k), v) for k,v in row.items())
        parent_id = fields.pop('parent_station', None)
        zone_id = fields.pop('zone_id', None)
        stop = Stop.objects.create(feed=feed, **fields)
        if parent_id:
            parent_of[parent_id].append(stop)
        if zone_id:
            zones[zone_id].append(stop)

    for parent_id, children in parent_of.items():
        parent = Stop.objects.get(feed=feed, stop_id=parent_id)
        for child in children:
            child.parent_station = parent
            child.save()
    for zone_id, stops in zones.items():
        zone, _c= Zone.objects.get_or_create(feed=feed, zone_id=zone_id)
        for stop in stops:
            stop.zone = zone
            stop.save()


def import_routes(routes_file, feed):
    """Import routes.txt into Route records for feed
    
    Keyword arguments:
    routes_file -- A open routes.txt for reading
    feed -- the Feed to associate the records with
    """
    reader = DictReader(routes_file)
    name_map = dict(route_short_name='short_name', route_long_name='long_name', 
                    route_desc='desc', route_type='rtype', route_url='url',
                    route_color='color', route_text_color='text_color')
    for row in reader:
        fields = dict((name_map.get(k, k), v) for k,v in row.items())
        agency_id = fields.pop('agency_id', None)
        if agency_id:
            agency = Agency.objects.get(feed=feed, agency_id=agency_id)
        else:
            agency = None
        route = Route.objects.create(feed=feed, agency=agency, **fields)

def import_trips(trips_file, feed):
    pass

def import_stop_times(stop_times_file, feed):
    pass

def import_calendar(calendar_file, feed):
    pass

def import_calendar_dates(calendar_dates_file, feed):
    pass

def import_fare_attributes(fare_attributes_file, feed):
    pass

def import_shapes(shapes_file, feed):
    pass

def import_frequencies(frequencies_file, feed):
    pass

def import_transfers(transfers_file, feed):
    pass

def import_feed_info(feed_info_file, feed):
    pass
