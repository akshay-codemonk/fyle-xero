import psycopg2
from django.db import IntegrityError
from django_q.models import Task
from django_q.tasks import async_task

from apps.fyle_expense.models import Expense, ExpenseGroup
from apps.xero_workspace.models import Invoice, InvoiceLineItem, EmployeeMapping, CategoryMapping, ProjectMapping
from apps.xero_workspace.utils import connect_to_fyle, connect_to_xero


def check_mappings(expense_group):
    mappings_error = ""
    employee_email = expense_group.description.get("employee_email")
    if not EmployeeMapping.objects.filter(workspace=expense_group.workspace,
                                          employee_email=employee_email).exists():
        mappings_error += f"Employee mapping missing for employee_email: {employee_email} \n"

        try:
            EmployeeMapping.objects.create(workspace=expense_group.workspace,
                                           employee_email=employee_email, invalid=True)
        except (psycopg2.errors.UniqueViolation, IntegrityError):
            pass

    for expense in expense_group.expenses.all():
        if not CategoryMapping.objects.filter(workspace=expense_group.workspace,
                                              category=expense.category).exists():
            mappings_error += f"Category mapping missing for category name: {expense.category} \n"

            try:
                CategoryMapping.objects.create(workspace=expense_group.workspace, category=expense.category,
                                               sub_category=expense.sub_category,
                                               invalid=True)
            except (psycopg2.errors.UniqueViolation, IntegrityError):
                pass

        if expense.project is not None:
            if not ProjectMapping.objects.filter(workspace=expense_group.workspace,
                                                 project_name=expense.project).exists():
                mappings_error += f"Project mapping missing for project_name: {expense.project}"

                try:
                    ProjectMapping.objects.create(workspace=expense_group.workspace,
                                                  project_name=expense.project, invalid=True)
                except (psycopg2.errors.UniqueViolation, IntegrityError):
                    pass

    if mappings_error:
        raise Exception(mappings_error)


def create_fetch_expense_task(workspace_id):
    """
    Create django Q task to pull expenses and sync to Xero
    :param workspace_id
    """
    kwargs = {"workspace_id": workspace_id}
    async_task(fetch_expenses_and_create_groups, **kwargs,
               q_options={"task_name": "Fetching Expenses",
                          "hook": "apps.task_log.hooks.update_fetch_expense_task",
                          }
               )


def create_invoice_task(expense_group_id):
    """
    Create django Q task to generate invoice and sync to Xero
    :param expense_group_id
    """
    kwargs = {"expense_group_id": expense_group_id}
    async_task(sync_to_xero, **kwargs,
               q_options={"task_name": "Creating Invoice",
                          "hook": "apps.task_log.hooks.update_create_invoice_task"
                          }
               )


def fetch_expenses_and_create_groups(workspace_id):
    """
    Fetch expenses, create expense groups and run an async
    task to sync with Xero
    :param workspace_id
    """
    updated_after = None
    latest_task = Task.objects.filter(tasklog__workspace__id=workspace_id, name="Fetching Expenses",
                                      success=True).last()
    if latest_task is not None:
        updated_after = latest_task.started
    expenses = Expense.fetch_paid_expenses(workspace_id, updated_after)
    expense_objects = Expense.create_expense_objects(expenses)
    connection = connect_to_fyle(workspace_id)
    expense_groups = ExpenseGroup.group_expense_by_report_id(expense_objects, workspace_id, connection)
    expense_group_objects = ExpenseGroup.create_expense_groups(expense_groups)
    for expense_group in expense_group_objects:
        create_invoice_task(expense_group.id)
    return workspace_id


def sync_to_xero(expense_group_id):
    """
    Generate invoice, invoice line items and post to Xero
    :param expense_group_id:
    :return:
    """
    expense_group = ExpenseGroup.objects.get(id=expense_group_id)
    check_mappings(expense_group)
    invoice_id = Invoice.create_invoice(expense_group)
    InvoiceLineItem.create_invoice_line_item(invoice_id, expense_group)
    xero = connect_to_xero(expense_group.workspace.id)
    invoice_data = generate_invoice_request_data(invoice_id)
    response = post_to_xero(invoice_data, xero)
    for invoice in response["Invoices"]:
        invoice_object = Invoice.objects.get(invoice_number=invoice["InvoiceNumber"])
        invoice_object.invoice_id = invoice["InvoiceID"]
        invoice_object.save()
    return expense_group_id


def generate_invoice_request_data(invoice_id):
    """
    Generate invoice request data as defined by Xero
    :param invoice_id
    :return: request_data
    """

    invoice = Invoice.objects.get(id=invoice_id)
    request_data = {
        "Type": "ACCPAY",
        "Contact": {
            "Name": invoice.contact_name,
        },
        "DateString": str(invoice.date),
        "InvoiceNumber": invoice.invoice_number,
        "LineAmountTypes": "Exclusive",
        "LineItems": []
    }

    for line_item in invoice.invoice_line_items.all():
        request_data["LineItems"].append({
            "Description": line_item.description,
            "Quantity": "1",
            "UnitAmount": str(line_item.amount),
            "AccountCode": str(line_item.account_code),
            "Tracking": [{
                "Name": line_item.tracking_category_name,
                "Option": line_item.tracking_category_option,
            }]
        })

    return request_data


def post_to_xero(data, xero):
    """ Makes an API call to create invoices in Xero
    :param data: Request data for the invoice API
    :param xero: Xero connection object
    :return response: response data from Xero API
    """
    response = xero.invoices.post(data)
    return response
