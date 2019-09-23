import tempfile
import shutil

import mock
from django.core.files import File
from django.test import TestCase, override_settings

from apps.sync_activity.models import Activity
from apps.user.models import UserProfile
from apps.xero_workspace.models import Workspace, XeroCredential, WorkspaceActivity

# Temporary media directory for tests
MEDIA_ROOT = tempfile.mkdtemp()


class WorkspaceTestCases(TestCase):
    """
    Test cases for Workspace model
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data
        """
        user = UserProfile.objects.create_user(email='user@test.com', password='foo')

        workspace = Workspace.objects.create(name='workspace1')
        workspace.user.add(user)

    def test_workspace_name_value(self):
        """
        Test for name valued
        """
        workspace = Workspace.objects.get(name='workspace1')
        self.assertEqual(workspace.name, 'workspace1')


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class XeroCredentialTestCases(TestCase):
    """
    Test cases for XeroCredential model
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data
        """
        pem_file = mock.MagicMock(spec=File)
        pem_file.name = 'file.pem'
        workspace = Workspace.objects.create(name='workspace1')

        XeroCredential.objects.create(pem_file=pem_file, consumer_key='consumer_key', workspace=workspace)

    def test_pem_file_value(self):
        """
        Test for pem_file value
        """
        xero_credential = XeroCredential.objects.get(id=1)
        self.assertEqual(xero_credential.pem_file.name, 'file.pem')

    def test_consumer_key_value(self):
        """
        Test for pem_file value
        """
        xero_credential = XeroCredential.objects.get(id=1)
        self.assertEqual(xero_credential.consumer_key, 'consumer_key')

    @classmethod
    def tearDownClass(cls):
        """
        Delete temporary directory
        """
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class WorkspaceActivityTestCases(TestCase):
    """
    Test cases for WorkspaceActivity model
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data
        """
        transform_sql_file = mock.MagicMock(spec=File)
        transform_sql_file.name = 'transform.sql'
        activity = Activity.objects.create(transform_sql=transform_sql_file)
        workspace = Workspace.objects.create(name='workspace1')

        WorkspaceActivity.objects.create(workspace=workspace, activity=activity)

    def test_workspace_activity_creation(self):
        """
        Test creation
        """
        workspace_activity = WorkspaceActivity.objects.get(id=1)
        self.assertEqual(workspace_activity.activity.transform_sql.name, 'transform.sql')

    @classmethod
    def tearDownClass(cls):
        """
        Delete temporary directory
        """
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()
