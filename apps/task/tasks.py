from django_q.models import Task
from django_q.tasks import async_task, result, Chain

from apps.expense.models import Expense, ExpenseGroup
from apps.task.models import TaskLog
from apps.xero_workspace.models import Workspace, Invoice, InvoiceLineItem
from apps.xero_workspace.utils import connect_to_fyle, connect_to_xero


def create_task_log(workspace_id, expense_group_id=None, chain=None):
    """
    Run async tasks and create task log object
    :param workspace_id
    :param expense_group_id
    :param chain
    :return
    """

    if expense_group_id is None:
        task_id = async_task(fetch_expenses_and_create_groups, workspace_id,
                             q_options={"task_name": "Fetching Expenses",
                                        "hook": "apps.task.hooks.update_fetch_expense_task"
                                        }
                             )
        TaskLog.objects.create(
            workspace=Workspace.objects.get(id=workspace_id),
            task_id=task_id
        )
    else:
        chain.append(sync_to_xero, expense_group_id,
                     q_options={"task_name": "Creating Invoice",
                                "hook": "apps.task.hooks.update_create_invoice_task"
                                }
                     )


def fetch_expenses_and_create_groups(workspace_id):
    """
    Fetch expenses, create expense groups and run a chain
    of async tasks to sync with Xero
    :param workspace_id
    """

    expenses = Expense.fetch_paid_expenses(workspace_id)
    expense_objects = Expense.create_expense_objects(expenses)
    connection = connect_to_fyle(workspace_id)
    expense_groups = ExpenseGroup.group_expense_by_report_id(expense_objects, workspace_id, connection)
    expense_group_objects = ExpenseGroup.create_expense_groups(expense_groups)
    chain = Chain()
    for expense_group in expense_group_objects:
        create_task_log(workspace_id, expense_group.id, chain)
    chain.run()


def sync_to_xero(expense_group_id):
    """
    Create invoice, invoice line items and post to Xero
    :param expense_group_id
    :return: expense_group_id
    """

    expense_group = ExpenseGroup.objects.get(id=expense_group_id)
    invoice_id = Invoice.create_invoice(expense_group)
    InvoiceLineItem.create_invoice_line_item(invoice_id, expense_group)
    xero = connect_to_xero(expense_group.workspace.id)
    invoice_data = generate_invoice_request_data(invoice_id)
    post_to_xero(invoice_data, xero)
    return expense_group_id


def generate_invoice_request_data(invoice_id):
    """
    Generate invoice request data as defined by Xero
    :param invoice_id
    :return: request_data
    """

    invoice = Invoice.objects.get(id=invoice_id)
    request_data = {
        "Type": "ACCREC",
        "Contact": {
            "Name": invoice.contact_name,
        },
        "DateString": str(invoice.date),
        "DueDateString": str(invoice.date),
        "InvoiceNumber": invoice.invoice_number,
        "LineItems": [],
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
