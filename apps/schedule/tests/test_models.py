import datetime

from dateutil.tz import UTC
from django.test import TestCase

from apps.schedule.models import Schedule


class ScheduleTestCases(TestCase):
    """
    Test cases for Schedule model
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data
        """
        Schedule.objects.create(
            start_at=datetime.datetime(year=2019, month=1, day=1, hour=6, minute=30, second=1, tzinfo=UTC),
            time_interval=5)
        Schedule.objects.create(start_at=datetime.datetime(year=2019, month=1, day=1, hour=6, tzinfo=UTC), enabled=True,
                                time_interval=500)

    def test_start_at_value(self):
        """
        Test start_at value
        """
        start_at = datetime.datetime(year=2019, month=1, day=1, hour=6, minute=30, second=1, tzinfo=UTC)
        schedule = Schedule.objects.get(id=1)
        self.assertEqual(schedule.start_at, start_at)

    def test_time_interval_value(self):
        """
        Test time_interval value
        """
        schedule = Schedule.objects.get(id=1)
        self.assertEqual(schedule.time_interval, 5)

    def test_default_enabled_value(self):
        """
        Test default enabled value
        """
        schedule = Schedule.objects.get(id=1)
        self.assertEqual(schedule.enabled, False)

    def test_enabled_value(self):
        """
        Test enabled value
        """
        schedule = Schedule.objects.get(id=2)
        self.assertEqual(schedule.enabled, True)
