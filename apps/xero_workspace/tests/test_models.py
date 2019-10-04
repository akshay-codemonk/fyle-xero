from django.test import TestCase

from apps.sync_activity.models import Activity
from apps.user.models import UserProfile
from apps.xero_workspace.models import Workspace, XeroCredential, WorkspaceActivity


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


class XeroCredentialTestCases(TestCase):
    """
    Test cases for XeroCredential model
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data
        """
        workspace = Workspace.objects.create(name='workspace1')

        XeroCredential.objects.create(private_key='private_key', consumer_key='consumer_key', workspace=workspace)

    def test_private_key_value(self):
        """
        Test for private_key value
        """
        xero_credential = XeroCredential.objects.get(id=1)
        self.assertEqual(xero_credential.private_key, 'private_key')

    def test_consumer_key_value(self):
        """
        Test for pem_file value
        """
        xero_credential = XeroCredential.objects.get(id=1)
        self.assertEqual(xero_credential.consumer_key, 'consumer_key')


class WorkspaceActivityTestCases(TestCase):
    """
    Test cases for WorkspaceActivity model
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data
        """
        activity = Activity.objects.create(transform_sql='transform_sql')
        workspace = Workspace.objects.create(name='workspace1')

        WorkspaceActivity.objects.create(workspace=workspace, activity=activity)

    def test_workspace_activity_creation(self):
        """
        Test creation
        """
        workspace_activity = WorkspaceActivity.objects.get(id=1)
        self.assertEqual(workspace_activity.activity.transform_sql, 'transform_sql')
