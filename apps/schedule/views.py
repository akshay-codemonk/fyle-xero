from django.shortcuts import render
from django.views import View


class ScheduleView(View):
    """
    Schedule View
    """
    template_name = "schedule/schedule.html"

    def get(self, request, workspace_id):
        context = {"schedule": "active"}
        return render(request, self.template_name, context)
