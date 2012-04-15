import StringIO

from django.test import TestCase

from multigtfs.models import Feed, Agency, Route
from multigtfs.utils import import_routes


class RouteTest(TestCase):
    def setUp(self):
        self.feed = Feed.objects.create()

    def test_string(self):
        route = Route.objects.create(feed=self.feed, route_id='RTEST', rtype=3)
        self.assertEqual(str(route), '1-RTEST')

    def test_import_routes_minimal(self):
        routes_txt = StringIO.StringIO("""\
route_id,route_short_name,route_long_name,route_type
AB,10,Airport - Bullfrog,3
""")
        import_routes(routes_txt, self.feed)
        route = Route.objects.get()
        self.assertEqual(route.feed, self.feed)
        self.assertEqual(route.route_id, 'AB')
        self.assertEqual(route.agency, None)
        self.assertEqual(route.short_name, '10')
        self.assertEqual(route.long_name, 'Airport - Bullfrog')
        self.assertEqual(route.desc, '')
        self.assertEqual(route.rtype, 3)
        self.assertEqual(route.url, '')
        self.assertEqual(route.color, '')
        self.assertEqual(route.text_color, '')

    def test_import_routes_maximal(self):
        routes_txt = StringIO.StringIO("""\
route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,\
route_url,route_color,route_text_color
AB,DTA,10,Airport - Bullfrog,"Our Airport Route", 3,http://example.com,\
00FFFF,000000
""")
        agency = Agency.objects.create(feed=self.feed, agency_id='DTA')
        import_routes(routes_txt, self.feed)
        route = Route.objects.get()
        self.assertEqual(route.feed, self.feed)
        self.assertEqual(route.route_id, 'AB')
        self.assertEqual(route.agency, agency)
        self.assertEqual(route.short_name, '10')
        self.assertEqual(route.long_name, 'Airport - Bullfrog')
        self.assertEqual(route.desc, 'Our Airport Route')
        self.assertEqual(route.rtype, 3)
        self.assertEqual(route.url, 'http://example.com')
        self.assertEqual(route.color, '00FFFF')
        self.assertEqual(route.text_color, '000000')
