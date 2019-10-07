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
        form = ScheduleForm(initial={'time_interval': schedule.time_interval})
        form.fields['start_at'].widget.js_options['defaultDate'] = schedule.start_at.strftime(
            '%Y-%m-%d %I:%M %p')
        context = {"schedule": "active", "workspace_id": workspace_id,
                   "workspace_name": workspace.name, "form": form,
                   "enabled": schedule.enabled}
        return render(request, self.template_name, context)

    def post(self, request, workspace_id):
        schedule = WorkspaceSchedule.objects.get(workspace__id=workspace_id).schedule
        datetime_str = request.POST['start_at']
        datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d %I:%M %p')
        time_interval = request.POST['time_interval']
        value = request.POST.get('schedule')
        schedule_enabled = False
        if value == 'enabled':
            schedule_enabled = True
        schedule.time_interval = time_interval
        schedule.start_at = make_aware(datetime_object)
        schedule.enabled = schedule_enabled
        schedule.save()

        return HttpResponseRedirect(self.request.path_info)
