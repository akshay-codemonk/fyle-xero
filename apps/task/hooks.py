from apps.task.models import TaskLog
from apps.xero_workspace.models import Invoice
from apps.expense.models import ExpenseGroup


def update_fetch_expense_task(task):
    task_log = TaskLog.objects.get(task_id=task.id)
    if task.success:
        task_log.level = 'Success'
        task_log.detail = task.result
        task_log.save()
    else:
        task_log.level = 'Fail'
        task_log.detail = task.result
        task_log.save()


def update_create_invoice_task(task):
    expense_group_id = task.result
    expense_group = ExpenseGroup.objects.get(id=expense_group_id)
    task_log = TaskLog.objects.create(
        workspace=expense_group.workspace,
        task_id=task.id,
        expense_group=expense_group
    )
    if task.success:
        task_log.invoice = expense_group.invoice
        task_log.level = 'Success'
        task_log.detail = task.result
        task_log.save()
    else:
        task_log.level = 'Fail'
        task_log.detail = task.result
        task_log.save()