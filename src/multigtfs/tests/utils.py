import os.path
import StringIO
import urllib

from django.test import TestCase

from multigtfs.models import Agency, Feed, Stop, Zone
from multigtfs.utils import (
    import_agency, import_gtfs, import_stops)

# Test GTFS data downloaded from
# http://timetablepublisher.googlecode.com/files/GTFS%20Test%20Data.zip
my_dir = os.path.dirname(__file__)
fix_dir = os.path.join(my_dir, 'fixtures')
test_path = os.path.abspath(os.path.join(fix_dir, 'GTFS_Test_Data.zip'))

class ImportGTFSTest(TestCase):

    def test_import_gtfs(self):
        feed = Feed.objects.create()
        with open(test_path, 'rb') as zip_file:
            import_gtfs(zip_file, feed)




