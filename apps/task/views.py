import json

from django.core import serializers
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from apps.task.models import TaskLog
from apps.task.tasks import create_task


class TaskLogView(View):
    """
    Task Log view
    """
    template_name = 'task/tasks.html'

    def get(self, request, workspace_id):
        context = {"tasks_tab": "active"}
        if request.GET.get('state') == 'complete':
            task_logs = TaskLog.objects.filter(workspace__id=workspace_id, task__success=True)
            context["complete"] = "active"
        elif request.GET.get('state') == 'failed':
            task_logs = TaskLog.objects.filter(workspace__id=workspace_id, task__success=False)
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
            create_task(workspace_id)
        return HttpResponseRedirect(self.request.path_info)


class TaskLogDetailsView(View):
    """
    Task log details view
    """

    @staticmethod
    def get(request, workspace_id, task_log_id):
        task_log = TaskLog.objects.get(id=task_log_id)
        serialized_task_log = json.loads(serializers.serialize('json', [task_log]))
        task_log_fields = {k: v for d in serialized_task_log for k, v in d.items()}["fields"]
        task_log_fields["task_name"] = task_log.task.name
        task_log_fields["status"] = 'Complete' if task_log.task.success else 'Failed'
        task_log_fields["started_at"] = task_log.task.started.strftime('%b. %d, %Y, %-I:%M %-p')
        task_log_fields["stopped_at"] = task_log.task.stopped.strftime('%b. %d, %Y, %-I:%M %p')
        task_log_fields["invoice"] = '-' if task_log.invoice is None else task_log.invoice.invoice_id
        task_log_fields["expense_group"] = '-' if task_log.expense_group is None else json.loads(
            task_log.expense_group.description).get('report_id')
        return JsonResponse(task_log_fields)
