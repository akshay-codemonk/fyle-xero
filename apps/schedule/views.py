from django.shortcuts import render
from django.views import View

from apps.xero_workspace.models import Workspace


class ScheduleView(View):
    """
    Schedule View
    """
    template_name = "schedule/schedule.html"

    def get(self, request, workspace_id):
        workspace_name = Workspace.objects.get(id=workspace_id).name
        context = {"schedule": "active", "workspace_id": workspace_id,
                   "workspace_name": workspace_name}
        return render(request, self.template_name, context)
