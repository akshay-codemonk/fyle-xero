import traceback

from apps.fyle_expense.models import Expense, ExpenseGroup
from apps.task_log.models import TaskLog
from apps.xero_workspace.utils import connect_to_fyle
from fyle_jobs import FyleJobsSDK
from fyle_xero_integration_web_app import settings


def schedule_expense_group_creation(workspace_id, user):
    fyle_sdk_connection = connect_to_fyle(workspace_id)

    jobs = FyleJobsSDK(settings.FYLE_JOBS_URL, fyle_sdk_connection)

    print("Creating task log..")
    task_log = TaskLog.objects.create(
        workspace_id=workspace_id,
        type="FETCHING EXPENSES",
        status="IN_PROGRESS"
    )

    print("Triggering job..")
    created_job = jobs.trigger_now(
        callback_url=f'{settings.API_BASE_URL}/workspace_jobs/{workspace_id}/expense_group/',
        callback_method='POST',
        object_id=task_log.id,
        payload={
            'task_log_id': task_log.id
        },
        job_description=f'Fetch expenses: Workspace id - {workspace_id}, user - {user}'
    )
    task_log.task_id = created_job['id']
    task_log.save()


def fetch_expenses_and_create_groups(workspace_id, task_log):
    """
    Fetch expenses and create expense groups
    """
    expense_group_ids = async_fetch_expenses_and_create_groups(workspace_id, task_log)
    print("Expense group ids return: ", expense_group_ids)
    task_log.detail = {
        'message': 'Creating expense groups'
    }
    task_log.save()

    if task_log.status == 'COMPLETE':
        # schedule_invoice_creation()
        print('Create invoice and invoice line items pending!')


def async_fetch_expenses_and_create_groups(workspace_id, task_log):
    """
    Fetch expenses, create expense groups and run an async
    task to sync with Xero
    :param workspace_id
    :param task_log
    """
    expense_group_ids = []
    print('async_fetch_expenses_and_create_groups')
    try:
        updated_after = None
        task_log = TaskLog.objects.filter(workspace__id=workspace_id).last()
        print("Task log: ", task_log)
        last_sync = task_log.created_at
        print("Last sync: ", )
        if last_sync is not None:
            updated_after = last_sync
        expenses = Expense.fetch_paid_expenses(workspace_id, updated_after)
        print("Expenses: ", expenses)
        expense_objects = Expense.create_expense_objects(expenses)
        print("Expense objects: ", expense_objects)
        connection = connect_to_fyle(workspace_id)
        print("Fyle conn: ", connection)
        expense_groups = ExpenseGroup.group_expense_by_report_id(expense_objects, workspace_id, connection)
        print("Expense groups: ", expense_groups)
        expense_group_objects = ExpenseGroup.create_expense_groups(expense_groups)
        print("Expense group objects: ", expense_group_objects)
        for expense_group in expense_group_objects:
            expense_group_ids.append(expense_group.id)
        print("Expense group ids: ", expense_group_ids)
        task_log.status = 'COMPLETE'
        task_log.save()
    except Exception:
        error = traceback.format_exc()
        print("Error: ", error)
        task_log.detail = {
            'error': error
        }
        task_log.status = 'FATAL'
        task_log.save()
    return expense_group_ids
