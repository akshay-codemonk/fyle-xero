from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views import View

from apps.task_log.models import TaskLog
from apps.task_log.tasks import schedule_expense_group_creation


class TaskLogView(View):
    """
    Task Log view
    """
    template_name = 'task/tasks.html'

    def get(self, request, workspace_id):
        context = {"tasks_tab": "active"}
        if request.GET.get('state') == 'complete':
            task_logs = TaskLog.objects.filter(workspace__id=workspace_id, status='COMPLETE')
            context["complete"] = "active"
        elif request.GET.get('state') == 'failed':
            task_logs = TaskLog.objects.filter(workspace__id=workspace_id, status='FATAL')
            context["failed"] = "active"
        else:
            task_logs = TaskLog.objects.filter(workspace__id=workspace_id)
            context["all"] = "active"

        page = request.GET.get('page', 1)
        paginator = Paginator(task_logs, 10)
        try:
            task_logs = paginator.page(page)
        except PageNotAnInteger:
            task_logs = paginator.page(1)
        except EmptyPage:
            task_logs = paginator.page(paginator.num_pages)

        context["task_logs"] = task_logs
        return render(request, self.template_name, context)

    def post(self, request, workspace_id):
        """
        Start synchronization
        :param request:
        :param workspace_id:
        :return:
        """
        value = request.POST.get('submit')
        if value == 'sync':
            schedule_expense_group_creation(workspace_id, request.user)
            messages.success(request, 'Sync started successfully. Expenses will be exported soon!')
        return HttpResponseRedirect(self.request.path_info)


class TaskLogDetailsView(View):
    """
    Task log details view
    """

    @staticmethod
    def get(request, workspace_id, task_log_id):
        task_log = TaskLog.objects.get(id=task_log_id)
        task_log_fields = model_to_dict(task_log)
        task_log_fields["task_id"] = task_log.task_id
        task_log_fields["type"] = task_log.type
        task_log_fields["status"] = task_log.status
        task_log_fields["started_at"] = task_log.created_at.strftime('%b. %d, %Y, %-I:%M %-p')
        task_log_fields["stopped_at"] = task_log.updated_at.strftime('%b. %d, %Y, %-I:%M %p')
        task_log_fields["invoice"] = '-' if task_log.invoice is None else task_log.invoice.invoice_id
        task_log_fields["expense_group"] = '-' if task_log.expense_group is None else task_log.expense_group. \
            description.get('report_id')
        return JsonResponse(task_log_fields)


class TaskLogTextView(View):
    """
    Task log text view
    """

    @staticmethod
    def get(request, workspace_id):
        task_log = None
        task_log_info = {}
        if request.GET.get('type') == "task_log":
            task_log_id = request.GET.get('id')
            task_log = TaskLog.objects.get(id=task_log_id)
        elif request.GET.get('type') == "expense_group":
            expense_group_id = request.GET.get('id')
            task_log = TaskLog.objects.filter(expense_group__id=expense_group_id).latest()

        task_log_info["workspace_name"] = task_log.workspace.name
        task_log_info["task_id"] = task_log.task_id
        task_log_info["type"] = task_log.type
        task_log_info["expense_group_id"] = '-' if task_log.expense_group is None else \
            task_log.expense_group.description.get("report_id")
        task_log_info["invoice_id"] = '-' if task_log.invoice is None else task_log.invoice.invoice_id
        task_log_info["task_start_time"] = task_log.created_at.strftime('%b. %d, %Y, %-I:%M %-p')
        task_log_info["task_stop_time"] = task_log.updated_at.strftime('%b. %d, %Y, %-I:%M %-p')
        task_log_info["status"] = task_log.status
        task_log_info["Task Result"] = task_log.detail
        return JsonResponse(task_log_info)
