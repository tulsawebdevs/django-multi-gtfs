from datetime import datetime, date
from collections import defaultdict
from csv import DictReader
from zipfile import ZipFile

from multigtfs.models import (
    Agency, Block, Fare, FareRule, Feed, FeedInfo, Frequency, Route, Service,
    ServiceDate, Shape, ShapePoint, Stop, StopTime, Transfer, Trip, Zone)

def import_gtfs(gtfs_file, feed):
    """Import a GTFS file as feed

    Keyword arguments:
    zip_file - A path or file-like object for the GTFS feed
    feed - The Feed to associate the GTFS data with

    Returns is a list of objects imported
    """
    z = ZipFile(gtfs_file, 'r')
    files = z.namelist()

    gtfs_order = (
        ('agency.txt', import_agency),
        ('stops.txt', import_stops),
        ('routes.txt', import_routes),
        ('calendar.txt', import_calendar),
        ('calendar_dates.txt', import_calendar_dates),
        ('shapes.txt', import_shapes),
        ('trips.txt', import_trips),
        ('stop_times.txt', import_stop_times),
        ('frequencies.txt', import_frequencies),
        ('fare_attributes.txt', import_fare_attributes),
        ('fare_rules.txt', import_fare_rules),
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
    name_map = dict(stop_code='code', stop_name='name', stop_desc='desc',
                    stop_lat='lat', stop_lon='lon', stop_url='url',
                    stop_timezone='timezone')
    for row in reader:
        fields = dict((name_map.get(k, k), v) for k,v in row.items())
        parent_id = fields.pop('parent_station', None)
        zone_id = fields.pop('zone_id', None)
        if zone_id:
            zone, _c =  Zone.objects.get_or_create(feed=feed, zone_id=zone_id)
        else:
            zone = None
        stop = Stop.objects.create(feed=feed, zone=zone, **fields)
        if parent_id:
            parent_of[parent_id].append(stop)

    for parent_id, children in parent_of.items():
        parent = Stop.objects.get(feed=feed, stop_id=parent_id)
        for child in children:
            child.parent_station = parent
            child.save()


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
        Route.objects.create(feed=feed, agency=agency, **fields)


def import_trips(trips_file, feed):
    """Import trips.txt into Trip records for feed
    
    Keyword arguments:
    trips_file -- A open trips.txt for reading
    feed -- the Feed to associate the records with
    """
    reader = DictReader(trips_file)
    name_map = dict(trip_headsign='headsign', trip_short_name='short_name',
                    direction_id='direction')
    for row in reader:
        fields = dict((name_map.get(k, k), v) for k,v in row.items())
        route_id = fields.pop('route_id')
        route = Route.objects.get(feed=feed, route_id=route_id)
        service_id = fields.pop('service_id')
        service = Service.objects.get(feed=feed, service_id=service_id)
        block_id = fields.pop('block_id', None)
        if block_id:
            block, _c = Block.objects.get_or_create(
                feed=feed, block_id=block_id)
        else:
            block = None
        shape_id = fields.pop('shape_id', None)
        if shape_id:
            shape = Shape.objects.get(feed=feed, shape_id=shape_id)
        else:
            shape = None
        trip_id = fields.pop('trip_id')
        trip, created = Trip.objects.get_or_create(
            trip_id=trip_id, route=route)
        for k,v in fields.items():
            if created:
                setattr(trip, k, v)
            else:
                assert getattr(trip, k) == v
        if created:
            trip.block = block
            trip.shape = shape
            trip.save()
        else:
            assert trip.block == block
            assert trip.shape == shape
        trip.services.add(service)


def import_stop_times(stop_times_file, feed):
    """Import stop_times.txt into StopTime records for feed
    
    Keyword arguments:
    stop_times_file -- A open stop_times.txt for reading
    feed -- the Feed to associate the records with
    """
    reader = DictReader(stop_times_file)
    name_map = dict(drop_off_time='drop_off_type')
    for row in reader:
        fields = dict((name_map.get(k, k), v) for k,v in row.items())
        trip_id = fields.pop('trip_id')
        trip = Trip.objects.get(route__feed=feed, trip_id=trip_id)
        stop_id = fields.pop('stop_id')
        stop = Stop.objects.get(feed=feed, stop_id=stop_id)
        # Turn None into blanks
        stop_headsign = fields.get('stop_headsign', '')
        fields['stop_headsign'] = stop_headsign or ''
        pickup_type = fields.get('pickup_type', '')
        fields['pickup_type'] = pickup_type or ''
        drop_off_type = fields.get('drop_off_type', '')
        fields['drop_off_type'] = drop_off_type or ''
        # Turn blanks into None
        arrival_time = fields.get('arrival_time', None)
        fields['arrival_time'] = arrival_time or None
        departure_time = fields.get('departure_time', None)
        fields['departure_time'] = departure_time or None
        shape_dist_traveled = fields.get('shape_dist_traveled', None)
        fields['shape_dist_traveled'] = shape_dist_traveled or None
        
        StopTime.objects.create(trip=trip, stop=stop, **fields)


def import_calendar(calendar_file, feed):
    """Import calendar.txt into Service records for feed
    
    Keyword arguments:
    calendar_file -- A open calendar.txt for reading
    feed -- the Feed to associate the records with
    """
    reader = DictReader(calendar_file)
    for row in reader:
        monday = row.pop('monday') == '1'
        tuesday = row.pop('tuesday') == '1'
        wednesday = row.pop('wednesday') == '1'
        thursday = row.pop('thursday') == '1'
        friday = row.pop('friday') == '1'
        saturday = row.pop('saturday') == '1'
        sunday = row.pop('sunday') == '1'
        start_date = datetime.strptime(row.pop('start_date'), '%Y%m%d')
        end_date = datetime.strptime(row.pop('end_date'), '%Y%m%d')
        
        Service.objects.create(
            feed=feed, monday=monday, tuesday=tuesday, wednesday=wednesday,
            thursday=thursday, friday=friday, saturday=saturday,
            sunday=sunday, start_date=start_date, end_date=end_date, **row)


def import_calendar_dates(calendar_dates_file, feed):
    """Import calendar_dates.txt into ServiceDate records for feed
    
    Keyword arguments:
    calendar_dates_file -- A open calendar_dates.txt for reading
    feed -- the Feed to associate the records with
    """
    reader = DictReader(calendar_dates_file)
    for row in reader:
        d = datetime.strptime(row.pop('date'), '%Y%m%d')
        service_id=row.pop('service_id')
        service = Service.objects.get(feed=feed, service_id=service_id)
        ServiceDate.objects.create(date=d, service=service, **row)


def import_frequencies(frequencies_file, feed):
    """Import frequencies.txt into Frequency records for feed
    
    Keyword arguments:
    frequencies_file -- A open frequencies.txt for reading
    feed -- the Feed to associate the records with
    """
    reader = DictReader(frequencies_file)
    for row in reader:
        trip_id = row.pop('trip_id')
        trip = Trip.objects.get(route__feed=feed, trip_id=trip_id)
        Frequency.objects.create(trip=trip, **row)


def import_fare_attributes(fare_attributes_file, feed):
    """Import fare_attributes.txt into FareAttributes records for feed
    
    Keyword arguments:
    fare_attributes_file -- A open fare_attributes.txt for reading
    feed -- the Feed to associate the records with
    """
    reader = DictReader(fare_attributes_file)
    for row in reader:
        transfer_duration = row.get('transfer_duration', None)
        row['transfer_duration'] = transfer_duration or None
        Fare.objects.create(feed=feed, **row)


def import_fare_rules(fare_rules_file, feed):
    """Import fare_rules.txt into FareRules records for feed
    
    Keyword arguments:
    fare_rules_file -- A open fare_rules.txt for reading
    feed -- the Feed to associate the records with
    """
    reader = DictReader(fare_rules_file)
    for row in reader:
        fare_id = row.pop('fare_id')
        fare = Fare.objects.get(feed=feed, fare_id=fare_id)
        route_id = row.pop('route_id', None)
        if route_id:
            route = Route.objects.get(feed=feed, route_id=route_id)
        else:
            route = None
        zone_origin_id = row.pop('origin_id', None)
        if zone_origin_id:
            zone_origin = Zone.objects.get(feed=feed, zone_id=zone_origin_id)
        else:
            zone_origin = None
        zone_dest_id = row.pop('destination_id', None)
        if zone_dest_id:
            zone_dest = Zone.objects.get(feed=feed, zone_id=zone_dest_id)
        else:
            zone_dest = None
        zone_cont_id = row.pop('contains_id', None)
        if zone_cont_id:
            zone_cont = Zone.objects.get(feed=feed, zone_id=zone_cont_id)
        else:
            zone_cont = None
        FareRule.objects.create(
            fare=fare, route=route, origin=zone_origin, destination=zone_dest,
            contains=zone_cont, **row)


def import_shapes(shapes_file, feed):
    """Import shapes.txt into Shape records for feed
    
    Keyword arguments:
    shapes_file -- A open shapes.txt for reading
    feed -- the Feed to associate the records with
    """
    reader = DictReader(shapes_file)
    name_map = dict(shape_pt_lat='lat', shape_pt_lon='lon',
                    shape_pt_sequence='sequence',
                    shape_dist_traveled='traveled')
    for row in reader:
        shape_id = row.pop('shape_id')
        shape, _c = Shape.objects.get_or_create(feed=feed, shape_id=shape_id)
        fields = dict((name_map.get(k, k), v) for k,v in row.items())
        # Force empty strings to None
        traveled = fields.get('traveled', None)
        fields['traveled'] = traveled or None
        ShapePoint.objects.create(shape=shape, **fields)


def import_transfers(transfers_file, feed):
    """Import transfers.txt into Transfer records for feed
    
    Keyword arguments:
    transfers_file -- A open transfers.txt for reading
    feed -- the Feed to associate the records with
    """
    reader = DictReader(transfers_file)
    for row in reader:
        from_stop_id = row.pop('from_stop_id')
        from_stop = Stop.objects.get(feed=feed, stop_id=from_stop_id)
        to_stop_id = row.pop('to_stop_id')
        to_stop = Stop.objects.get(feed=feed, stop_id=to_stop_id)
        # Force empty strings to 0, None
        transfer_type = row.pop('transfer_type', None)
        row['transfer_type'] = transfer_type or 0
        min_transfer_time = row.pop('min_transfer_time', None)
        row['min_transfer_time'] = min_transfer_time or None
        Transfer.objects.create(from_stop=from_stop, to_stop=to_stop, **row)


def import_feed_info(feed_info_file, feed):
    """Import feed_info.txt into a FeedInfo record for feed
    
    Keyword arguments:
    feed_info_file -- A open transfers.txt for reading
    feed -- the Feed to associate the records with
    """
    reader = DictReader(feed_info_file)
    name_map = dict(feed_publisher_name='publisher_name',
                    feed_publisher_url='publisher_url', feed_lang='lang',
                    feed_start_date='start_date', feed_end_date='end_date',
                    feed_version='version')
    for row in reader:
        fields = dict((name_map.get(k, k), v) for k,v in row.items())
        start_date_raw = fields.pop('start_date', None)
        if start_date_raw:
            start_date = datetime.strptime(start_date_raw, '%Y%m%d')
        else:
            start_date = None
        end_date_raw = fields.pop('end_date', None)
        if end_date_raw:
            end_date = datetime.strptime(end_date_raw, '%Y%m%d')
        else:
            end_date = None
        
        FeedInfo.objects.create(feed=feed, start_date=start_date,
            end_date=end_date, **fields)
