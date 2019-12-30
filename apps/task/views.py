from django.shortcuts import render
from django.views import View


class TaskLogView(View):
    """
    Task Log view
    """
    template_name = 'task/tasks.html'

    def get(self, request, workspace_id):
        context = {"tasks_tab": "active", "tasks": "active"}
        return render(request, self.template_name, context)
