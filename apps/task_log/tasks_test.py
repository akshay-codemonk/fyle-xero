import traceback

import psycopg2
from django.db import IntegrityError

from apps.fyle_expense.models import Expense, ExpenseGroup
from apps.task_log.models import TaskLog
from apps.xero_workspace.models import EmployeeMapping, CategoryMapping, ProjectMapping, Invoice, InvoiceLineItem
from apps.xero_workspace.utils import connect_to_fyle, connect_to_xero
from fyle_jobs import FyleJobsSDK
from fyle_xero_integration_web_app import settings


def schedule_expense_group_creation(workspace_id, user):
    fyle_sdk_connection = connect_to_fyle(workspace_id)

    jobs = FyleJobsSDK(settings.FYLE_JOBS_URL, fyle_sdk_connection)

    task_log = TaskLog.objects.create(
        workspace_id=workspace_id,
        type="FETCHING EXPENSES",
        status="IN_PROGRESS"
    )

    created_job = jobs.trigger_now(
        callback_url=f'{settings.API_BASE_URL}/workspace_jobs/{workspace_id}/expense_group/trigger/',
        callback_method='POST',
        object_id=task_log.id,
        payload={
            'task_log_id': task_log.id
        },
        job_description=f'Fetch expenses: Workspace id - {workspace_id}, user - {user}'
    )
    task_log.task_id = created_job['id']
    task_log.save()


def schedule_invoice_creation(workspace_id, expense_group_ids, user):
    expense_groups = ExpenseGroup.objects.filter(
        workspace_id=workspace_id, id__in=expense_group_ids).all()
    fyle_sdk_connection = connect_to_fyle(workspace_id)
    jobs = FyleJobsSDK(settings.FYLE_JOBS_URL, fyle_sdk_connection)

    for expense_group in expense_groups:
        task_log, _ = TaskLog.objects.update_or_create(
            workspace_id=expense_group.workspace.id,
            expense_group=expense_group,
            type='CREATING INVOICE',
            status='IN_PROGRESS'
        )
        created_job = jobs.trigger_now(
            callback_url='{0}{1}'.format(
                settings.API_BASE_URL,
                '/workspace_jobs/{0}/expense_group/{1}/invoice/trigger/'.format(
                    workspace_id,
                    expense_group.id
                )
            ),
            callback_method='POST',
            object_id=task_log.id,
            payload={
                'task_log_id': task_log.id
            },
            job_description=f'Create invoice: Workspace id - {workspace_id}, \
            user - {user}, expense group id - {expense_group.id}'
        )
        task_log.task_id = created_job['id']
        task_log.save()


def fetch_expenses_and_create_groups(workspace_id, task_log, user):
    """
    Fetch expenses and create expense groups
    """
    expense_group_ids = async_fetch_expenses_and_create_groups(workspace_id, task_log)

    if task_log.status == 'COMPLETE':
        schedule_invoice_creation(workspace_id, expense_group_ids, user)

    return task_log


def async_fetch_expenses_and_create_groups(workspace_id, task_log):
    """
    Fetch expenses, create expense groups and run an async
    task to sync with Xero
    :param workspace_id
    :param task_log
    """
    expense_group_ids = []
    try:
        updated_at = None
        latest_task_log = TaskLog.objects.filter(workspace__id=workspace_id, type='FETCHING EXPENSES',
                                                 status='COMPLETE').latest()
        if latest_task_log is not None:
            updated_at = latest_task_log.created_at
        expenses = Expense.fetch_paid_expenses(workspace_id, updated_at)
        expense_objects = Expense.create_expense_objects(expenses)
        connection = connect_to_fyle(workspace_id)
        expense_groups = ExpenseGroup.group_expense_by_report_id(expense_objects, workspace_id, connection)
        expense_group_objects = ExpenseGroup.create_expense_groups(expense_groups)
        for expense_group in expense_group_objects:
            expense_group_ids.append(expense_group.id)
        task_log.status = 'COMPLETE'
        task_log.detail = 'Expense groups created successfully!'
        task_log.save()
    except Exception:
        error = traceback.format_exc()
        task_log.detail = {
            'error': error
        }
        task_log.status = 'FATAL'
        task_log.save()
    return expense_group_ids


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


def async_create_invoice_and_post_to_xero(expense_group, task_log):
    try:
        check_mappings(expense_group)
        invoice_id = Invoice.create_invoice(expense_group)
        InvoiceLineItem.create_invoice_line_item(invoice_id, expense_group)
        xero_sdk_connection = connect_to_xero(expense_group.workspace.id)
        invoice_obj = Invoice.objects.get(id=invoice_id)
        invoice_data = generate_invoice_request_data(invoice_obj)
        response = post_invoice(invoice_data, xero_sdk_connection)
        for invoice in response["Invoices"]:
            invoice_obj.invoice_id = invoice["InvoiceID"]
            invoice_obj.save()
        task_log.invoice = invoice_obj
        task_log.detail = 'Invoice created successfully!'
        task_log.status = 'COMPLETE'
        task_log.save()
    except Exception:
        error = traceback.format_exc()
        task_log.detail = {
            'error': error
        }
        task_log.status = 'FATAL'
        task_log.save()


def generate_invoice_request_data(invoice):
    """
    Generate invoice request data as defined by Xero
    :param invoice
    :return: request_data
    """

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


def post_invoice(data, xero):
    """ Makes an API call to create invoices in Xero
    :param data: Request data for the invoice API
    :param xero: Xero connection object
    :return response: response data from Xero API
    """
    response = xero.invoices.post(data)
    return response
