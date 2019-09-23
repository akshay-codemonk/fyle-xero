import shutil
import tempfile

import mock
from django.core.files import File
from django.test import TestCase, override_settings

from apps.sync_activity.models import Activity
from fyle_xero_integration_web_app import settings

# Temporary media directory for tests
MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ActivityTestCases(TestCase):
    """
    Test cases for Activity model
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data
        """
        settings.MEDIA_ROOT = tempfile.mkdtemp()

        transform_sql_file = mock.MagicMock(spec=File)
        transform_sql_file.name = 'transform.sql'

        sync_db_file = mock.MagicMock(spec=File)
        sync_db_file.name = 'sqlite.db'

        success = Activity.STATUS.success
        triggerd_by = Activity.TRIGGERS.user

        Activity.objects.create(transform_sql=transform_sql_file, status=success, triggered_by=triggerd_by,
                                sync_db=sync_db_file, request_data={"request": 1}, response_data={"response": 1},
                                error_msg='error')
        Activity.objects.create(transform_sql=transform_sql_file)

    def test_transform_sql_value(self):
        """
        Test transform_sql value
        """
        activity = Activity.objects.get(id=1)
        self.assertEqual(activity.transform_sql.name, 'transform.sql')

    def test_sync_db_value(self):
        """
        Test sync_db value
        """
        activity = Activity.objects.get(id=1)
        self.assertEqual(activity.sync_db.name, 'sqlite.db')

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
        self.assertEqual(activity.request_data, {"request": 1})

    def test_response_data_value(self):
        """
        Test response_data value
        """
        activity = Activity.objects.get(id=1)
        self.assertEqual(activity.response_data, {"response": 1})

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

    @classmethod
    def tearDownClass(cls):
        """
        Delete temporary directory
        """
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()
