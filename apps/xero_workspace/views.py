import ast

import openpyxl
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from apps.xero_workspace.forms import XeroCredentialsForm, CategoryMappingForm, EmployeeMappingForm, TransformForm
from apps.xero_workspace.models import Workspace, WorkspaceActivity, XeroCredential, FyleCredential
from apps.xero_workspace.utils import upload_file_to_aws


class WorkspaceView(View):
    """
    Workspace Dashboard view
    """
    template_name = "xero_workspace/workspace.html"

    def get(self, request):
        present_workspaces = Workspace.objects.filter(user=request.user).values('id', 'name', 'user')
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
        if form.is_valid:
            refresh_token = FyleCredential.objects.get(workspace__id=workspace_id).fyle_auth.refresh_token
            consumer_key = request.POST['consumer_key']
            file_id = upload_file_to_aws(request.FILES, refresh_token)
            XeroCredential.objects.create(file_id=file_id, consumer_key=consumer_key,
                                          workspace=Workspace.objects.get(id=workspace_id))
        elif value == "disconnect":
            XeroCredential.objects.get(workspace__id=workspace_id).delete()

        return HttpResponseRedirect(self.request.path_info)


class CategoryMappingView(LoginRequiredMixin, View):
    """
    Category Mapping View
    """
    template_name = "xero_workspace/category_mapping.html"

    def get(self, request, workspace_id):
        form = CategoryMappingForm()
        workspace = Workspace.objects.get(id=workspace_id)
        context = {"category_mapping": "active", "workspace_id": workspace_id,
                   "workspace_name": workspace.name, "form": form,
                   "category_account": workspace.category_account}
        return render(request, self.template_name, context)

    def post(self, request, workspace_id):
        value = request.POST.get('submit')
        workspace = Workspace.objects.get(id=workspace_id)
        if value == 'delete':
            selected_mappings = [ast.literal_eval(x) for x in request.POST.getlist('selected-mappings')]
            workspace.category_account['mappings'] = [i for i in workspace.category_account['mappings'] if
                                                      i not in selected_mappings]
            workspace.save()
        elif value == 'upload':
            file = request.FILES['bulk_upload_file']
            wb = openpyxl.load_workbook(file)
            worksheet = wb.active
            for c1, c2 in worksheet.iter_rows(min_row=2):
                new_mapping = {
                    "category_name": str(c1.value),
                    "account_code": str(c2.value).split('.')[0],
                }
                workspace.category_account['mappings'] = [i for i in workspace.category_account['mappings'] if
                                                          not (i["category_name"] == new_mapping["category_name"])]
                workspace.category_account['mappings'].append(new_mapping)
            workspace.save()
        else:
            form = CategoryMappingForm(request.POST)
            if form.is_valid:
                new_mapping = {
                    "category_name": request.POST['category_name'],
                    "account_code": request.POST['account_code']
                }
                workspace.category_account["mappings"].append(new_mapping)
                workspace.save()

        return HttpResponseRedirect(self.request.path_info)


class EmployeeMappingView(LoginRequiredMixin, View):
    """
    Employee Mapping View
    """
    template_name = "xero_workspace/employee_mapping.html"

    def get(self, request, workspace_id):
        form = EmployeeMappingForm()
        workspace = Workspace.objects.get(id=workspace_id)
        context = {"employee_mapping": "active", "workspace_id": workspace_id,
                   "workspace_name": workspace.name, "form": form,
                   "employee_contact": workspace.employee_contact}
        return render(request, self.template_name, context)

    def post(self, request, workspace_id):
        value = request.POST.get('submit')
        workspace = Workspace.objects.get(id=workspace_id)
        if value == 'delete':
            selected_mappings = [ast.literal_eval(x) for x in request.POST.getlist('selected-mappings')]
            workspace.employee_contact['mappings'] = [i for i in workspace.employee_contact['mappings'] if
                                                      i not in selected_mappings]
            workspace.save()
        elif value == 'upload':
            file = request.FILES['bulk_upload_file']
            wb = openpyxl.load_workbook(file)
            worksheet = wb.active
            for c1, c2 in worksheet.iter_rows(min_row=2):
                new_mapping = {
                    "employee_name": str(c1.value),
                    "contact_email": str(c2.value),
                }
                workspace.employee_contact['mappings'] = [i for i in workspace.employee_contact['mappings'] if
                                                          not (i["employee_name"] == new_mapping["employee_name"])]
                workspace.employee_contact['mappings'].append(new_mapping)
            workspace.save()
        else:
            form = EmployeeMappingForm(request.POST)
            if form.is_valid:
                new_mapping = {
                    "employee_name": request.POST['employee_name'],
                    "contact_email": request.POST['contact_email']
                }
                workspace.employee_contact["mappings"].append(new_mapping)
                workspace.save()

        return HttpResponseRedirect(self.request.path_info)


class TransformView(LoginRequiredMixin, View):
    """
    Transform View
    """
    template_name = "xero_workspace/transform.html"

    def get(self, request, workspace_id):
        form = TransformForm()
        workspace = Workspace.objects.get(id=workspace_id)
        if workspace.transform_sql is not None:
            form.fields['transform_sql'].initial = workspace.transform_sql
        context = {"transform": "active", "workspace_id": workspace_id,
                   "workspace_name": workspace.name, "form": form}
        return render(request, self.template_name, context)

    def post(self, request, workspace_id):
        workspace = Workspace.objects.get(id=workspace_id)
        value = request.POST.get('submit')
        if value == 'edit':
            form = TransformForm()
            if workspace.transform_sql is not None:
                form.fields['transform_sql'].initial = workspace.transform_sql
            form.fields['transform_sql'].widget.attrs['disabled'] = False
            save_button = True
            context = {"transform": "active", "workspace_id": workspace_id,
                       "workspace_name": workspace.name, "form": form,
                       "save_button": save_button}
            return render(request, self.template_name, context)
        if value == 'save':
            form = TransformForm(request.POST)
            if form.is_valid:
                workspace.transform_sql = request.POST['transform_sql']
                workspace.save()
        return HttpResponseRedirect(self.request.path_info)
