from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views import View
from django_q.tasks import async_task

from apps.sync_activity.models import Activity
from apps.xero_workspace.hooks import update_activity_status
from apps.xero_workspace.models import Workspace, WorkspaceActivity
from apps.xero_workspace.tasks import sync_xero


class SyncActivityView(View):
    """
    Sync Activity View
    """
    template_name = "sync_activity/activity.html"
    workspace = None
    context = None

    def setup(self, request, *args, **kwargs):
        workspace_id = kwargs['workspace_id']
        self.workspace = Workspace.objects.get(id=workspace_id)
        workspace_activity = Activity.objects.filter(activities__workspace__id=workspace_id).order_by(
            '-updated_at')
        self.context = {"activity": "active", "workspace_activity": workspace_activity}
        super(SyncActivityView, self).setup(request)

    def get(self, request, workspace_id):
        workspace_activity = Activity.objects.filter(activities__workspace__id=workspace_id).order_by('-updated_at')
        page = request.GET.get('page', 1)
        paginator = Paginator(workspace_activity, 10)
        try:
            workspace_activity = paginator.page(page)
        except PageNotAnInteger:
            workspace_activity = paginator.page(1)
        except EmptyPage:
            workspace_activity = paginator.page(paginator.num_pages)
        self.context['workspace_activity'] = workspace_activity
        return render(request, self.template_name, self.context)

    def post(self, request, workspace_id):
        value = request.POST.get('submit')
        if value == 'sync':
            activity = Activity.objects.create(transform_sql=self.workspace.transform_sql,
                                               error_msg='Synchronisation in progress')
            activity_id = activity.id
            WorkspaceActivity.objects.create(workspace=self.workspace, activity=activity)
            async_task(sync_xero, workspace_id, activity_id, hook=update_activity_status)
            return render(request, self.template_name, self.context)
        return render(request, self.template_name, self.context)
