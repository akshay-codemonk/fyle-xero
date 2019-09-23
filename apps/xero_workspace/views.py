from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from apps.xero_workspace.forms import XeroCredentialsForm
from apps.xero_workspace.models import Workspace, WorkspaceActivity, XeroCredential


class WorkspaceView(View):
    """
    Workspace Dashboard view
    """
    template_name = "xero_workspace/workspace.html"

    def get(self, request):
        present_workspaces = Workspace.objects.filter(user=request.user).values('id', 'name',
                                                                                'user')

        for workspace in present_workspaces:
            try:
                workspace_last_sync = WorkspaceActivity.objects.get(
                    workspace__name=workspace['name']).activity.updated_at
                workspace['last_sync'] = workspace_last_sync
            except ObjectDoesNotExist:
                workspace['last_sync'] = '-'
        return render(request, self.template_name,
                      {"workspaces": present_workspaces, })

    def post(self, request):
        new_workspace_name = request.POST.get('new-workspace-name')
        instance = Workspace.objects.create(name=new_workspace_name)
        instance.user.add(request.user)
        instance.save()
        return redirect('/workspace')


class XeroConnect(LoginRequiredMixin, View):
    """
    Xero (destination) connect View
    """
    template_name = "xero_workspace/destination_connect.html"

    def get(self, request, workspace_id):
        form = XeroCredentialsForm()
        is_connected = XeroCredential.objects.filter(workspace__id=workspace_id).exists()
        workspace_name = Workspace.objects.get(id=workspace_id).name
        context = {"destination": "active", "workspace_id": workspace_id,
                   "workspace_name": workspace_name, "form": form, "is_connected": is_connected}
        return render(request, self.template_name, context)

    def post(self, request, workspace_id):
        value = request.POST.get('type')
        if value == "connect":
            form = XeroCredentialsForm(request.POST, request.FILES)
            workspace = Workspace.objects.get(id=workspace_id)
            if form.is_valid():
                post = form.save(commit=False)
                post.workspace = workspace
                post.save()
        elif value == "disconnect":
            XeroCredential.objects.get(workspace__id=workspace_id).delete()

        return HttpResponseRedirect(self.request.path_info)


class CategoryMappingView(LoginRequiredMixin, View):
    """
    Category Mapping View
    """
    template_name = "xero_workspace/category_mapping.html"

    def get(self, request, workspace_id):
        workspace_name = Workspace.objects.get(id=workspace_id).name
        context = {"category_mapping": "active", "workspace_id": workspace_id,
                   "workspace_name": workspace_name}
        return render(request, self.template_name, context)


class EmployeeMappingView(LoginRequiredMixin, View):
    """
    Employee Mapping View
    """
    template_name = "xero_workspace/employee_mapping.html"

    def get(self, request, workspace_id):
        workspace_name = Workspace.objects.get(id=workspace_id).name
        context = {"employee_mapping": "active", "workspace_id": workspace_id,
                   "workspace_name": workspace_name}
        return render(request, self.template_name, context)


class TransformView(LoginRequiredMixin, View):
    """
    Transform View
    """
    template_name = "xero_workspace/transform.html"

    def get(self, request, workspace_id):
        workspace_name = Workspace.objects.get(id=workspace_id).name
        context = {"transform": "active", "workspace_id": workspace_id,
                   "workspace_name": workspace_name}
        return render(request, self.template_name, context)
