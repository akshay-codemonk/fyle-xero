from datetime import datetime

import pytz
from django.test import TestCase

from apps.fyle_connect.models import FyleAuth
from apps.xero_connect.models import XeroAuth
from apps.user.models import UserProfile
from apps.xero_workspace.models import Workspace, XeroCredential, WorkspaceSchedule, EmployeeMapping, \
    CategoryMapping, FyleCredential, ProjectMapping, Invoice, InvoiceLineItem


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
        xero_auth = XeroAuth.objects.create(client_id='12345', client_secret='abcd#1234', refresh_token='qwerty')
        XeroCredential.objects.create(xero_auth=xero_auth, workspace=workspace)

    def test_xero_credential_creation(self):
        """
        Test model creation
        """
        xero_credential = XeroCredential.objects.get(id=1)
        self.assertEqual(xero_credential.workspace.name, 'workspace1')

    def test_string_representation(self):
        """
        Test model string representation
        """
        xero_credential = XeroCredential.objects.get(id=1)
        self.assertEqual(str(xero_credential), '1')


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


class ProjectMappingTestCases(TestCase):
    """
    Test cases for ProjectMapping model
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data
        """
        workspace = Workspace.objects.create(name='workspace1')
        ProjectMapping.objects.create(project_name='project',
                                      tracking_category_name='tracking_category_name',
                                      tracking_category_option='tracking_category_option',
                                      workspace=workspace)

    def test_project_mapping_creation(self):
        """
        Test project mapping creation
        """
        project_mapping = ProjectMapping.objects.get(id=1)
        self.assertEqual(project_mapping.workspace.name, 'workspace1')

    def test_string_representation(self):
        """
        Test model string representation
        """
        project_mapping = ProjectMapping.objects.get(id=1)
        self.assertEqual(str(project_mapping), '1')


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
    Test cases for the WorkspaceSchedule model
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data
        """
        Workspace.objects.create(name='schedule_creation')

    def test_workspace_schedule_creation(self):
        """
        Test creation
        """
        workspace_schedule = WorkspaceSchedule.objects.get(workspace__name='schedule_creation')
        self.assertEqual(workspace_schedule.workspace.name, 'schedule_creation')


class InvoiceTestCases(TestCase):
    """
    Invoice model test cases
    """

    @classmethod
    def setUpTestData(cls):
        Invoice.objects.create(
            invoice_number="inv123",
            contact_name="employee",
            date=datetime.now(tz=pytz.utc),
            description="rep123"
        )

    def test_invoice_creation(self):
        """
        Test invoice creation
        """
        invoice = Invoice.objects.get(invoice_number="inv123")
        self.assertEqual(invoice.contact_name, "employee")


class InvoiceLineItemTestCases(TestCase):
    """
    InvoiceLineItem model test cases
    """

    @classmethod
    def setUpTestData(cls):
        invoice = Invoice.objects.create(
            invoice_number="inv123",
            contact_name="employee",
            date=datetime.now(tz=pytz.utc),
            description="rep123"
        )
        InvoiceLineItem.objects.create(
            invoice=invoice,
            account_code=123,
            account_name="acc_name",
            description="rep123",
            amount=100.00
        )

    def test_invoice_lineitem_creation(self):
        """
        Test invoice lineitem creation
        """
        invoice_lineitem = InvoiceLineItem.objects.get(account_code=123)
        self.assertEqual(invoice_lineitem.account_name, "acc_name")
