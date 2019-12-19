from datetime import datetime

import pytz
from django.test import TestCase

from apps.expense.models import Expense, ExpenseGroup
from apps.xero_workspace.models import Workspace


class ExpenseTestCases(TestCase):
    """
    Test cases for Expense model
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data
        """
        Expense.objects.create(
            employee_email="employee@test.in",
            expense_id="exp123",
            expense_number="exp/num/123",
            amount=499.50,
            settlement_id="set123",
            report_id="rep123",
            expense_created_at=datetime.now(tz=pytz.utc),
            spent_at=datetime.now(tz=pytz.utc),
            reimbursable=True,
            state="PAID",
        )

    def test_expense_creation(self):
        """
        Test expense creation
        """
        expense = Expense.objects.all()

        expense = Expense.objects.get(employee_email="employee@test.in")
        self.assertEqual(expense.expense_id, "exp123")

    def test_string_representation(self):
        """
        Test model string representation
        """
        expense = Expense.objects.get(employee_email="employee@test.in")
        self.assertEqual(str(expense), "exp123")


class ExpenseGroupTestCases(TestCase):
    """
    Test cases for ExpenseGroup model
    """

    @classmethod
    def setUpTestData(cls):
        workspace = Workspace.objects.create(name='test_workspace')
        expense_group = ExpenseGroup.objects.create(workspace=workspace,
                                                    description="rep123")
        expense = Expense.objects.create(
            employee_email="employee@test.in",
            expense_id="exp123",
            expense_number="exp/num/123",
            amount=499.50,
            settlement_id="set123",
            report_id="rep123",
            expense_created_at=datetime.now(tz=pytz.utc),
            spent_at=datetime.now(tz=pytz.utc),
            reimbursable=True,
            state="PAID",
        )
        expense_group.expenses.add(expense)

    def test_expense_group_creation(self):
        """
        Test expense group creation
        """
        expense_group = ExpenseGroup.objects.get(id=1)
        self.assertEqual(expense_group.workspace.name, "test_workspace")

    def test_string_representation(self):
        """
        Test model string representation
        """
        expense_group = ExpenseGroup.objects.get(id=1)
        self.assertEqual(str(expense_group), "1")
