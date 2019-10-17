from django.test import TestCase

from apps.sync_activity.models import Activity


class ActivityTestCases(TestCase):
    """
    Test cases for Activity model
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data
        """

        success = Activity.STATUS.success
        triggerd_by = Activity.TRIGGERS.user

        Activity.objects.create(transform_sql='transform_sql', status=success, triggered_by=triggerd_by,
                                sync_db_file_id='1a2b', request_data='{request: 1}', response_data='{response: 1}',
                                error_msg='error')
        Activity.objects.create()

    def test_transform_sql_value(self):
        """
        Test transform_sql value
        """
        activity = Activity.objects.get(id=1)
        self.assertEqual(activity.transform_sql, 'transform_sql')

    def test_sync_db_value(self):
        """
        Test sync_db_file_id value
        """
        activity = Activity.objects.get(id=1)
        self.assertEqual(activity.sync_db_file_id, '1a2b')

    def test_status_value(self):
        """
        Test status value
        """
        activity = Activity.objects.get(id=1)
        self.assertEqual(activity.status, 'success')

    def test_triggered_by_value(self):
        """
        Test triggered_by value
        """
        activity = Activity.objects.get(id=1)
        self.assertEqual(activity.triggered_by, 'user')

    def test_request_data_value(self):
        """
        Test request_data value
        """
        activity = Activity.objects.get(id=1)
        self.assertEqual(activity.request_data, '{request: 1}')

    def test_response_data_value(self):
        """
        Test response_data value
        """
        activity = Activity.objects.get(id=1)
        self.assertEqual(activity.response_data, '{response: 1}')

    def test_default_status_value(self):
        """
        Test default status value
        """
        activity = Activity.objects.get(id=2)
        self.assertEqual(activity.status, 'in_progress')

    def test_default_triggered_by_value(self):
        """
        Test default triggered_by value
        """
        activity = Activity.objects.get(id=2)
        self.assertEqual(activity.triggered_by, 'user')
