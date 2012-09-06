from django.test import TestCase

from multigtfs.models.fields import GTFSSeconds, GTFSSecondsField


class GTFSSecondsTest(TestCase):

    def test_string(self):
        self.assertEqual(u'00:00:00', unicode(GTFSSeconds(0)))
        self.assertEqual(u'24:00:00', unicode(GTFSSeconds(24 * 60 * 60)))
        self.assertEqual('12:34:56', str(GTFSSeconds(45296)))

    def test_negative_seconds_raises(self):
        self.assertRaises(ValueError, GTFSSeconds, -1)

    def test_from_hms(self):
        standard = GTFSSeconds(45296)
        from_hms = GTFSSeconds.from_hms(hours=12, minutes=34, seconds=56)
        self.assertEqual(standard, from_hms)

    def test_unequal_int(self):
        seconds = GTFSSeconds(1000)
        self.assertNotEqual(seconds, 1000)

    def test_ordering(self):
        one_minute = GTFSSeconds(60)
        one_hour = GTFSSeconds(3600)
        one_hour2 = GTFSSeconds(3600)
        self.assertTrue(one_hour > one_minute)
        self.assertFalse(one_hour > one_hour2)
        self.assertTrue(one_hour >= one_hour2)
        self.assertTrue(one_hour == one_hour2)


class GTFSSecondsFieldTest(TestCase):

    def setUp(self):
        self.f = GTFSSecondsField()

    def test_to_python_int(self):
        self.assertEqual(GTFSSeconds(400), self.f.to_python(400))

    def test_to_python_GTFSSeconds(self):
        self.assertEqual(GTFSSeconds(500), self.f.to_python(GTFSSeconds(500)))

    def test_to_python_seconds_string(self):
        self.assertEqual(GTFSSeconds(500), self.f.to_python('500'))

    def test_to_python_hm_string(self):
        self.assertEqual(GTFSSeconds(3660), self.f.to_python('01:01'))

    def test_to_python_hms_string(self):
        self.assertEqual(GTFSSeconds(3661), self.f.to_python('01:01:01'))

    def test_to_python_too_many_colons(self):
        self.assertRaises(ValueError, self.f.to_python, '01:01:01:01')

    def test_prep_db_value_GTFSSeconds(self):
        self.assertEqual(500, self.f.get_prep_value(GTFSSeconds(500)))

    def test_prep_db_value_None(self):
        self.assertIsNone(self.f.get_prep_value(None))
