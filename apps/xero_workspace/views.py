import ast

import openpyxl
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from apps.xero_workspace.forms import XeroCredentialsForm, CategoryMappingForm, EmployeeMappingForm, TransformForm
from apps.xero_workspace.models import Workspace, WorkspaceActivity, XeroCredential


class WorkspaceView(View):
    """
    Workspace Dashboard view
    """
    template_name = "xero_workspace/workspace.html"

    def get(self, request):
        user_workspaces = Workspace.objects.filter(user=request.user)
        for workspace in user_workspaces:
            try:
                workspace.last_sync = WorkspaceActivity.objects.filter(workspace=workspace).latest(
                    'activity__updated_at').activity.updated_at
            except WorkspaceActivity.DoesNotExist:
                workspace.last_sync = '-'
        return render(request, self.template_name, {"workspaces": user_workspaces})

    def post(self, request):
        new_workspace_name = request.POST.get('new-workspace-name')
        instance = Workspace.objects.create(name=new_workspace_name)
        instance.user.add(request.user)
        instance.save()
        return HttpResponseRedirect(self.request.path_info)


class DestinationView(View):
    """
    Destination (xero) view
    """
    template_name = "xero_workspace/destination.html"

    def get(self, request, workspace_id):
        form = XeroCredentialsForm()
        is_connected = XeroCredential.objects.filter(workspace__id=workspace_id).exists()
        context = {"destination": "active", "form": form, "is_connected": is_connected}
        return render(request, self.template_name, context)


class XeroConnectView(View):
    """
    Xero (destination) connect view
    """

    @staticmethod
    def post(request, workspace_id):
        form = XeroCredentialsForm(request.POST, request.FILES)
        if form.is_valid:
            consumer_key = request.POST['consumer_key']
            private_key = str(request.FILES['pem_file'].read(), 'utf-8')
            XeroCredential.objects.create(private_key=private_key, consumer_key=consumer_key,
                                          workspace=Workspace.objects.get(id=workspace_id))
        return HttpResponseRedirect(reverse('xero_workspace:destination', args=[workspace_id]))


class XeroDisconnectView(View):
    """
    Xero (destination) disconnect view
    """

    @staticmethod
    def post(request, workspace_id):
        XeroCredential.objects.get(workspace__id=workspace_id).delete()
        return HttpResponseRedirect(reverse('xero_workspace:destination', args=[workspace_id]))


class CategoryMappingView(View):
    """
    Category Mapping View
    """
    template_name = "xero_workspace/category_mapping.html"
    workspace = None

    def dispatch(self, request, *args, **kwargs):
        method = self.request.POST.get('method', '').lower()
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(CategoryMappingView, self).dispatch(request, *args, **kwargs)

    def setup(self, request, *args, **kwargs):
        workspace_id = kwargs['workspace_id']
        self.workspace = Workspace.objects.get(id=workspace_id)
        super(CategoryMappingView, self).setup(request)

    def get(self, request, workspace_id):
        form = CategoryMappingForm()
        context = {"category_mapping": "active", "form": form,
                   "category_account": self.workspace.category_account}
        return render(request, self.template_name, context)

    def post(self, request, workspace_id):
        form = CategoryMappingForm(request.POST)
        if form.is_valid:
            new_mapping = {
                "category_name": request.POST['category_name'],
                "account_code": request.POST['account_code']
            }
            self.workspace.category_account["mappings"].append(new_mapping)
            self.workspace.save()
        return HttpResponseRedirect(self.request.path_info)

    def delete(self, request, workspace_id):
        selected_mappings = [ast.literal_eval(x) for x in request.POST.getlist('selected-mappings')]
        self.workspace.category_account['mappings'] = [i for i in self.workspace.category_account['mappings'] if
                                                       i not in selected_mappings]
        self.workspace.save()
        return HttpResponseRedirect(self.request.path_info)


class CategoryMappingBulkUploadView(View):
    """
    Category mapping bulk upload view
    """

    @staticmethod
    def post(request, workspace_id):
        workspace = Workspace.objects.get(id=workspace_id)
        file = request.FILES['bulk_upload_file']
        work_book = openpyxl.load_workbook(file)
        worksheet = work_book.active
        for column_1, column_2 in worksheet.iter_rows(min_row=2):
            new_mapping = {
                "category_name": str(column_1.value),
                "account_code": str(column_2.value).split('.')[0],
            }
            workspace.category_account['mappings'] = [i for i in workspace.category_account['mappings'] if
                                                      not i["category_name"] == new_mapping["category_name"]]
            workspace.category_account['mappings'].append(new_mapping)
        workspace.save()
        return HttpResponseRedirect(reverse('xero_workspace:category_mapping', args=[workspace_id]))


class EmployeeMappingView(View):
    """
    Employee Mapping View
    """
    template_name = "xero_workspace/employee_mapping.html"
    workspace = None

    def setup(self, request, *args, **kwargs):
        workspace_id = kwargs['workspace_id']
        self.workspace = Workspace.objects.get(id=workspace_id)
        super(EmployeeMappingView, self).setup(request)

    def dispatch(self, request, *args, **kwargs):
        method = self.request.POST.get('method', '').lower()
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(EmployeeMappingView, self).dispatch(request, *args, **kwargs)

    def get(self, request, workspace_id):
        form = EmployeeMappingForm()
        context = {"employee_mapping": "active", "form": form,
                   "employee_contact": self.workspace.employee_contact}
        return render(request, self.template_name, context)

    def post(self, request, workspace_id):
        form = EmployeeMappingForm(request.POST)
        if form.is_valid:
            new_mapping = {
                "employee_name": request.POST['employee_name'],
                "contact_email": request.POST['contact_email']
            }
            self.workspace.employee_contact["mappings"].append(new_mapping)
            self.workspace.save()
        return HttpResponseRedirect(self.request.path_info)

    def delete(self, request, workspace_id):
        selected_mappings = [ast.literal_eval(x) for x in request.POST.getlist('selected-mappings')]
        self.workspace.employee_contact['mappings'] = [i for i in self.workspace.employee_contact['mappings'] if
                                                       i not in selected_mappings]
        self.workspace.save()
        return HttpResponseRedirect(self.request.path_info)


class EmployeeMappingBulkUploadView(View):
    """
    Employee mapping bulk upload view
    """

    @staticmethod
    def post(request, workspace_id):
        workspace = Workspace.objects.get(id=workspace_id)
        file = request.FILES['bulk_upload_file']
        work_book = openpyxl.load_workbook(file)
        worksheet = work_book.active
        for column_1, column_2 in worksheet.iter_rows(min_row=2):
            new_mapping = {
                "employee_name": str(column_1.value),
                "contact_email": str(column_2.value),
            }
            workspace.employee_contact['mappings'] = [i for i in workspace.employee_contact['mappings'] if
                                                      not i["employee_name"] == new_mapping["employee_name"]]
            workspace.employee_contact['mappings'].append(new_mapping)
        workspace.save()
        return HttpResponseRedirect(reverse('xero_workspace:employee_mapping', args=[workspace_id]))


class TransformView(View):
    """
    Transform View
    """
    template_name = "xero_workspace/transform.html"
    context = None
    workspace = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        method = self.request.POST.get('method', '').lower()
        if method == 'update':
            return self.update(*args, **kwargs)
        return super(TransformView, self).dispatch(request, *args, **kwargs)

    def setup(self, request, *args, **kwargs):
        workspace_id = kwargs['workspace_id']
        self.form = TransformForm()
        self.workspace = Workspace.objects.get(id=workspace_id)
        if self.workspace.transform_sql is not None:
            self.form.fields['transform_sql'].initial = self.workspace.transform_sql
        self.context = {"transform": "active", "form": self.form}
        super(TransformView, self).setup(request)

    def get(self, request, workspace_id):
        return render(request, self.template_name, self.context)

    def post(self, request, workspace_id):
        self.form = TransformForm(request.POST)
        if self.form.is_valid:
            self.workspace.transform_sql = request.POST['transform_sql']
            self.workspace.save()
        return HttpResponseRedirect(self.request.path_info)

    def update(self, request, workspace_id):
        self.form.fields['transform_sql'].widget.attrs['disabled'] = False
        self.context['save_button'] = True
        return render(request, self.template_name, self.context)
