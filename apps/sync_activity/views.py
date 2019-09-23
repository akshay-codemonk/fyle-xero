from django.shortcuts import render
from django.views import View

from apps.xero_workspace.models import Workspace


class SyncActivityView(View):
    """
    Sync Activity View
    """
    template_name = "sync_activity/activity.html"

    def get(self, request, workspace_id):
        workspace_name = Workspace.objects.get(id=workspace_id).name
        context = {"activity": "active", "workspace_id": workspace_id,
                   "workspace_name": workspace_name}
        return render(request, self.template_name, context)
