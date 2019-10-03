import ast

import openpyxl
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from apps.xero_workspace.forms import XeroCredentialsForm, CategoryMappingForm, EmployeeMappingForm, TransformForm
from apps.xero_workspace.models import Workspace, WorkspaceActivity, XeroCredential, CategoryMapping, EmployeeMapping


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
            return self.delete(request, *args, **kwargs)
        return super(CategoryMappingView, self).dispatch(request, *args, **kwargs)

    def setup(self, request, *args, **kwargs):
        workspace_id = kwargs['workspace_id']
        self.workspace = Workspace.objects.get(id=workspace_id)
        super(CategoryMappingView, self).setup(request)

    def get(self, request, workspace_id):
        form = CategoryMappingForm()
        context = {"category_mapping": "active", "form": form,
                   "mappings": CategoryMapping.objects.filter(workspace__id=workspace_id)}
        return render(request, self.template_name, context)

    def post(self, request, workspace_id):
        form = CategoryMappingForm(request.POST)
        if form.is_valid:
            category = request.POST['category']
            sub_category = request.POST['sub_category']
            account_code = request.POST['account_code']
            CategoryMapping.objects.create(workspace=self.workspace, category=category, sub_category=sub_category,
                                           account_code=account_code)
            self.workspace.save()
        return HttpResponseRedirect(self.request.path_info)

    def delete(self, request, workspace_id):
        selected_mappings = [ast.literal_eval(x) for x in request.POST.getlist('mapping_ids')]
        CategoryMapping.objects.filter(id__in=selected_mappings).delete()
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
        category_objects = []
        for category, sub_category, account_code in worksheet.iter_rows(min_row=2):
            sub_category.value = '' if sub_category.value is None else sub_category.value
            category_objects.append(
                CategoryMapping(workspace=workspace, category=category.value, sub_category=sub_category.value,
                                account_code=account_code.value))
        CategoryMapping.objects.bulk_create(category_objects)
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
            return self.delete(request, *args, **kwargs)
        return super(EmployeeMappingView, self).dispatch(request, *args, **kwargs)

    def get(self, request, workspace_id):
        form = EmployeeMappingForm()
        context = {"employee_mapping": "active", "form": form,
                   "mappings": EmployeeMapping.objects.filter(workspace__id=workspace_id)}
        return render(request, self.template_name, context)

    def post(self, request, workspace_id):
        form = EmployeeMappingForm(request.POST)
        if form.is_valid:
            employee_email = request.POST['employee_email']
            contact_name = request.POST['contact_name']
            EmployeeMapping.objects.create(workspace=self.workspace, employee_email=employee_email,
                                           contact_name=contact_name)
        return HttpResponseRedirect(self.request.path_info)

    def delete(self, request, workspace_id):
        selected_mappings = [ast.literal_eval(x) for x in request.POST.getlist('mapping_ids')]
        EmployeeMapping.objects.filter(id__in=selected_mappings).delete()
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
        employee_mapping_objects = []
        for employee_email, contact_name in worksheet.iter_rows(min_row=2):
            employee_mapping_objects.append(
                EmployeeMapping(workspace=workspace, employee_email=employee_email.value,
                                contact_name=contact_name.value))
        EmployeeMapping.objects.bulk_create(employee_mapping_objects)
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
