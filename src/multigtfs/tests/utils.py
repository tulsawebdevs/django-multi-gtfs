from datetime import time

from django.test import TestCase

from multigtfs.utils import parse_time


class ParseTimeTest(TestCase):
    def test_null(self):
        t, d = parse_time(None)
        self.assertEqual(t, None)
        self.assertEqual(d, None)

    def test_blank(self):
        t, d = parse_time('')
        self.assertEqual(t, None)
        self.assertEqual(d, None)

    def test_standard(self):
        t, d = parse_time('08:30:14')
        self.assertEqual(t, time(8, 30, 14))
        self.assertEqual(d, 0)

    def test_next_day(self):
        t, d = parse_time('24:30:14')
        self.assertEqual(t, time(0, 30, 14))
        self.assertEqual(d, 1)
