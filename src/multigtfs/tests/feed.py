import StringIO

from django.test import TestCase

from multigtfs.models import Feed


class FeedModelTest(TestCase):
    def test_string(self):
        feed = Feed.objects.create()
        self.assertEqual(feed.id, 1)
        self.assertEqual(str(feed), '1')
        feed.name = 'Test'
        self.assertEqual(str(feed), '1 Test')
