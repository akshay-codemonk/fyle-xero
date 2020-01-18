from django.core.mail import send_mail

from apps.expense.models import ExpenseGroup
from apps.task.models import TaskLog
from apps.xero_workspace.models import Workspace, Invoice
from fyle_xero_integration_web_app.settings import SENDER_EMAIL


def update_fetch_expense_task(task):
    """
    Update task log fields of "Fetching Expenses" task
    :param task: Task object
    """

    workspace_id = task.kwargs.get("workspace_id")
    workspace = Workspace.objects.get(id=workspace_id)
    task_log = TaskLog.objects.create(
        workspace=workspace,
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
        send_mail(
            'Error fetching expenses from Fyle',
            task.result,
            SENDER_EMAIL,
            [workspace.user.all().first().email],
            fail_silently=False,
        )


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
    if task.success:
        task_log.invoice = expense_group.invoice
        task_log.level = '-'
        task_log.detail = task.result
        task_log.save()
    else:
        Invoice.delete_invoice(expense_group)
        task_log.level = 'Error'
        task_log.detail = task.result
        task_log.save()
        send_mail('Error fetching expenses from Fyle', task.result,
                  SENDER_EMAIL,
                  [expense_group.workspace.user.all().first().email],
                  fail_silently=False,
                  )
