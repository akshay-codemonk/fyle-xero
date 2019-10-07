from _datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.timezone import make_aware
from django.views import View

from apps.schedule.forms import ScheduleForm
from apps.xero_workspace.models import Workspace, WorkspaceSchedule


class ScheduleView(View):
    """
    Schedule View
    """
    template_name = "schedule/schedule.html"

    def get(self, request, workspace_id):
        workspace = Workspace.objects.get(id=workspace_id)
        schedule = WorkspaceSchedule.objects.get(workspace__id=workspace_id).schedule
        form = ScheduleForm(initial={'minutes': schedule.minutes})
        form.fields['next_run'].widget.js_options['defaultDate'] = schedule.next_run.strftime(
            '%Y-%m-%d %I:%M %p')
        context = {"schedule": "active", "workspace_id": workspace_id,
                   "workspace_name": workspace.name, "form": form,
                   "enabled": schedule.repeats}
        return render(request, self.template_name, context)

    def post(self, request, workspace_id):
        schedule = WorkspaceSchedule.objects.get(workspace__id=workspace_id).schedule
        datetime_str = request.POST['next_run']
        datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d %I:%M %p')
        minutes = request.POST['minutes']
        value = request.POST.get('schedule')
        schedule_enabled = 0
        if value == 'enabled':
            schedule_enabled = -1
        schedule.minutes = minutes
        schedule.next_run = make_aware(datetime_object)
        schedule.repeats = schedule_enabled
        schedule.save()

        return HttpResponseRedirect(self.request.path_info)
