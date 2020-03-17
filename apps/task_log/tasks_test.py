import traceback

from apps.fyle_expense.models import Expense, ExpenseGroup
from apps.task_log.models import TaskLog
from apps.xero_workspace.models import Workspace
from apps.xero_workspace.utils import connect_to_fyle
from fyle_jobs import FyleJobsSDK


def schedule_expense_group_creation(workspace_id, user):
    fyle_sdk_connection = connect_to_fyle(workspace_id)

    jobs = FyleJobsSDK("https://jobs.staging.fyle.in/v2/jobs", fyle_sdk_connection)

    print("Creating task log..")
    task_log = TaskLog.objects.create(
        workspace_id=workspace_id,
        type="FETCHING EXPENSES",
        status="IN_PROGRESS"
    )

    print("Triggering job..")
    created_job = jobs.trigger_now(
        callback_url=f'http://localhost:8000/workspace/{workspace_id}/expense_groups/task/',
        callback_method='POST',
        object_id=task_log.id,
        payload={
            'task_log_id': task_log.id
        },
        job_description=f'Fetch expenses: Workspace id - {workspace_id}, user - {user}',
        # job_data_url=f'http://localhost:8000/workspace/{workspace_id}/expense_groups/task/',
    )
    task_log.task_id = created_job['id']
    task_log.save()


def fetch_expenses_and_create_groups(workspace_id, task_log):
    """
    Fetch expenses and create expense groups
    """
    async_fetch_expenses_and_create_groups(workspace_id, task_log)
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
        workspace = Workspace.objects.get(id=workspace_id)
        last_sync = workspace.last_sync
        if last_sync is not None:
            updated_after = last_sync
        expenses = Expense.fetch_paid_expenses(workspace_id, updated_after)
        expense_objects = Expense.create_expense_objects(expenses)
        connection = connect_to_fyle(workspace_id)
        expense_groups = ExpenseGroup.group_expense_by_report_id(expense_objects, workspace_id, connection)
        expense_group_objects = ExpenseGroup.create_expense_groups(expense_groups)
        for expense_group in expense_group_objects:
            expense_group_ids.append(expense_group.id)
        task_log.status = 'COMPLETE'
        task_log.save()
    except Exception:
        error = traceback.format_exc()
        task_log.detail = {
            'error': error
        }
        task_log.status = 'FATAL'
        task_log.save()
    return expense_group_ids
