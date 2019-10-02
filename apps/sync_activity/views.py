from django.shortcuts import render
from django.views import View


class SyncActivityView(View):
    """
    Sync Activity View
    """
    template_name = "sync_activity/activity.html"

    def get(self, request, workspace_id):
        context = {"activity": "active"}
        return render(request, self.template_name, context)
