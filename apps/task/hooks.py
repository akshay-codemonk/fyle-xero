from apps.expense.models import ExpenseGroup
from apps.task.models import TaskLog
from apps.xero_workspace.models import Workspace


def update_fetch_expense_task(task):
    """
    Update task log fields of "Fetching Expenses" task
    :param task: Task object
    """

    workspace_id = task.kwargs.get("workspace_id")
    task_log = TaskLog.objects.create(
        workspace=Workspace.objects.get(id=workspace_id),
        task_id=task.id
    )
    if task.success:
        task_log.level = '-'
        task_log.detail = task.result
        task_log.save()
    else:
        task_log.level = 'Error'
        task_log.detail = task.result
        task_log.save()


def update_create_invoice_task(task):
    """
    Update task log fields of "Creating Invoice" task
    :param task: Task object
    """
    expense_group_id = task.kwargs.get("expense_group_id")
    expense_group = ExpenseGroup.objects.get(id=expense_group_id)
    task_log = TaskLog.objects.create(
        workspace=expense_group.workspace,
        task_id=task.id
    )

    task_log.expense_group = expense_group
    task_log.invoice = expense_group.invoice
    if task.success:
        task_log.level = '-'
        task_log.detail = task.result
        task_log.save()
    else:
        task_log.level = 'Error'
        task_log.detail = task.result
        task_log.save()
