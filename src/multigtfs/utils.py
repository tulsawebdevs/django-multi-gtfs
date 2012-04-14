import csv
import zipfile

from models import Agency, Stop, Zone

def import_gtfs(gtfs_file, feed):
    """Import a GTFS file as feed
    
    Keyword arguments:
    zip_file - A path or file-like object for the GTFS feed
    feed - The Feed to associate the GTFS data with
    
    Returns is a list of objects imported
    """
    z = zipfile.ZipFile(gtfs_file, 'r')
    files = z.namelist()
    print files
    
    gtfs_order = (
        ('agency.txt', import_agency),
        ('stops.txt', import_stops),
    )

    objects = []
    for table_name, importer in gtfs_order:
        for f in files:
            if f.endswith(table_name):
                table = z.open(f)
                objects.extend(importer(table, feed))
    return objects

def import_agency(agency_file, feed):
    """Import agency.txt into Agency record for feed.
    
    Keyword arguments:
    agency_file -- A open agency.txt for reading
    feed -- the Feed to associate the records with
    
    Return is a list of agency records created.
    """
    reader = csv.DictReader(agency_file)
    agencies = []
    name_map = dict(agency_url='url', agency_name='name',
                    agency_phone='phone', agency_fare_url='fare_url',
                    agency_timezone='timezone', agency_lang='lang')
    for row in reader:
        fields = dict((name_map.get(k, k), v) for k,v in row.items())
        agency = Agency.objects.create(feed=feed, **fields)
        agencies.append(agency)
    return agencies

def import_stops(stops_file, feed):
    """Import stops.txt into Stop record for feed
    
    Keyword arguments:
    stops_file -- A open stops.txt for reading
    feed -- the Feed to associate the records with
    
    Zone objects may also be created, if referenced in the stops
    
    Return is a list of stop records created (but not zone records).
    """
    reader = csv.DictReader(stops_file)
    stops = []
    zones = dict()
    name_map = dict(stop_code='code', stop_name='name', stop_desc='desc', 
                    stop_lat='lat', stop_lon='lon', stop_url='url',
                    stop_timezone='timezone')
    for row in reader:
        fields = dict((name_map.get(k, k), v) for k,v in row.items())
        parent_id = fields.pop('parent_station', None)
        if parent_id:
            parent = Stop.objects.get(feed=feed, stop_id=parent_id)
        else:
            parent = None
        zone_id = fields.pop('zone_id', None)
        if zone_id:
            if not zone_id in zones:
                zone, created = Zone.objects.get_or_create(
                    feed=feed, zone_id=zone_id)
                zones[zone_id] = zone
            else:
                zone = zones.get(zone_id)
        else:
            zone = None
        stop = Stop.objects.create(
            feed=feed, parent_station=parent, zone=zone, **fields)
        stops.append(stop)
    return stops
