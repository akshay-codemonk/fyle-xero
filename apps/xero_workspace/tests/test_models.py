import datetime

from django.test import TestCase
from django_q.models import Schedule

from apps.fyle_connect.models import FyleAuth
from apps.sync_activity.models import Activity
from apps.user.models import UserProfile
from apps.xero_workspace.models import Workspace, XeroCredential, WorkspaceActivity, WorkspaceSchedule, EmployeeMapping, \
    CategoryMapping, FyleCredential


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

    def test_string_representation(self):
        """
        Test model string representation
        """
        workspace = Workspace.objects.get(name='workspace1')
        self.assertEqual(str(workspace), 'workspace1')


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

    def test_string_representation(self):
        """
        Test model string representation
        """
        xero_credential = XeroCredential.objects.get(id=1)
        self.assertEqual(str(xero_credential), '1')


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

    def test_string_representation(self):
        """
        Test model string representation
        """
        workspace_activity = WorkspaceActivity.objects.get(id=1)
        self.assertEqual(str(workspace_activity), '1')


class EmployeeMappingTestCases(TestCase):
    """
    Test model string representation
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data
        """
        workspace = Workspace.objects.create(name='workspace1')
        EmployeeMapping.objects.create(employee_email='emp@test.com', contact_name='contact', workspace=workspace)

    def test_employee_mapping_creation(self):
        """
        Test creation
        """
        employee_mapping = EmployeeMapping.objects.get(id=1)
        self.assertEqual(employee_mapping.workspace.name, 'workspace1')

    def test_string_representation(self):
        """
        Test model string representation
        """
        employee_mapping = EmployeeMapping.objects.get(id=1)
        self.assertEqual(str(employee_mapping), '1')


class CategoryMappingTestCases(TestCase):
    """
    Test model string representation
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data
        """
        workspace = Workspace.objects.create(name='workspace1')
        CategoryMapping.objects.create(category='category', sub_category='sub_category', account_code=1,
                                       workspace=workspace)

    def test_category_mapping_creation(self):
        """
        Test creation
        """
        category_mapping = CategoryMapping.objects.get(id=1)
        self.assertEqual(category_mapping.workspace.name, 'workspace1')

    def test_string_representation(self):
        """
        Test model string representation
        """
        category_mapping = CategoryMapping.objects.get(id=1)
        self.assertEqual(str(category_mapping), '1')


class FyleCredentialTestCases(TestCase):
    """
    Test model string representation
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data
        """
        workspace = Workspace.objects.create(name='workspace1')
        fyle_auth = FyleAuth.objects.create(client_id='12345', client_secret='abcd#1234', refresh_token='qwerty')
        FyleCredential.objects.create(fyle_auth=fyle_auth, workspace=workspace)

    def test_fyle_credential_creation(self):
        """
        Test creation
        """
        fyle_credential = FyleCredential.objects.get(id=1)
        self.assertEqual(fyle_credential.workspace.name, 'workspace1')

    def test_string_representation(self):
        """
        Test model string representation
        """
        fyle_credential = FyleCredential.objects.get(id=1)
        self.assertEqual(str(fyle_credential), '1')


class WorkspaceScheduleTestCases(TestCase):
    """
    Test cases for the WorksapceSchedule model
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data
        """
        workspace = Workspace.objects.create(name='workspace1')
        schedule = Schedule.objects.create(func='module.tasks.function', schedule_type=Schedule.MINUTES,
                                           repeats=0, minutes=5, next_run=datetime.datetime.now())
        WorkspaceSchedule.objects.create(workspace=workspace, schedule=schedule)

    def test_workspace_schedule_creation(self):
        """
        Test creation
        """
        workspace_schedule = WorkspaceSchedule.objects.get(id=1)
        self.assertEqual(workspace_schedule.schedule.id, 1)

    def test_string_representation(self):
        """
        Test model string representation
        """
        workspace_schedule = WorkspaceSchedule.objects.get(id=1)
        self.assertEqual(str(workspace_schedule), '1')
