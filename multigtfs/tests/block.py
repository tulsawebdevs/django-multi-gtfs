from django.test import TestCase

from multigtfs.models import Block, Feed


class BlockTest(TestCase):
    def test_string(self):
        feed = Feed.objects.create()
        self.assertEqual(feed.id, 1)
        block = Block.objects.create(feed=feed, block_id='BTEST')
        self.assertEqual(str(block), '1-BTEST')
