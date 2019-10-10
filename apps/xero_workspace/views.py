import ast
from datetime import datetime

import openpyxl
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.timezone import make_aware
from django.views import View

from apps.xero_workspace.forms import XeroCredentialsForm, CategoryMappingForm, EmployeeMappingForm, TransformForm, \
    ScheduleForm
from apps.xero_workspace.models import Workspace, WorkspaceActivity, XeroCredential, CategoryMapping, EmployeeMapping, \
    WorkspaceSchedule
from apps.xero_workspace.utils import create_workspace


class WorkspaceView(View):
    """
    Workspace Dashboard view
    """
    template_name = "xero_workspace/workspace.html"

    def dispatch(self, request, *args, **kwargs):
        method = self.request.POST.get('method', '').lower()
        if method == 'delete':
            return self.delete(request)
        return super(WorkspaceView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        user_workspaces = Workspace.objects.filter(user=request.user).order_by('-created_at')
        page = request.GET.get('page', 1)
        paginator = Paginator(user_workspaces, 10)
        try:
            user_workspaces = paginator.page(page)
        except PageNotAnInteger:
            user_workspaces = paginator.page(1)
        except EmptyPage:
            user_workspaces = paginator.page(paginator.num_pages)
        for workspace in user_workspaces:
            try:
                workspace.last_sync = WorkspaceActivity.objects.filter(workspace=workspace).latest(
                    'activity__updated_at').activity.updated_at
            except WorkspaceActivity.DoesNotExist:
                workspace.last_sync = '-'
        return render(request, self.template_name, {"workspaces": user_workspaces})

    def post(self, request):
        workspace_name = request.POST.get('new-workspace-name')
        workspace = create_workspace(workspace_name=workspace_name)
        workspace.user.add(request.user)
        workspace.save()
        return HttpResponseRedirect(self.request.path_info)

    def delete(self, request):
        selected_workspace = [ast.literal_eval(x) for x in request.POST.getlist('workspace_ids')]
        Workspace.objects.filter(id__in=selected_workspace).delete()
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
            consumer_key = request.POST.get('consumer_key')
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
        category_mappings = CategoryMapping.objects.filter(workspace__id=workspace_id).order_by('-created_at')
        page = request.GET.get('page', 1)
        paginator = Paginator(category_mappings, 10)
        try:
            category_mappings = paginator.page(page)
        except PageNotAnInteger:
            category_mappings = paginator.page(1)
        except EmptyPage:
            category_mappings = paginator.page(paginator.num_pages)
        form = CategoryMappingForm()
        context = {"category_mapping": "active", "form": form,
                   "mappings": category_mappings}
        return render(request, self.template_name, context)

    def post(self, request, workspace_id):
        form = CategoryMappingForm(request.POST)
        if form.is_valid:
            category = request.POST.get('category')
            sub_category = request.POST.get('sub_category')
            account_code = request.POST.get('account_code')
            category_mapping, created = CategoryMapping.objects.get_or_create(workspace=self.workspace,
                                                                              category=category)
            category_mapping.sub_category = sub_category
            category_mapping.account_code = account_code
            category_mapping.save()
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
        employee_mappings = EmployeeMapping.objects.filter(workspace__id=workspace_id).order_by('-created_at')
        page = request.GET.get('page', 1)
        paginator = Paginator(employee_mappings, 10)
        try:
            employee_mappings = paginator.page(page)
        except PageNotAnInteger:
            employee_mappings = paginator.page(1)
        except EmptyPage:
            employee_mappings = paginator.page(paginator.num_pages)
        form = EmployeeMappingForm()
        context = {"employee_mapping": "active", "form": form,
                   "mappings": employee_mappings}
        return render(request, self.template_name, context)

    def post(self, request, workspace_id):
        form = EmployeeMappingForm(request.POST)
        if form.is_valid:
            employee_email = request.POST.get('employee_email')
            contact_name = request.POST.get('contact_name')
            employee_mapping, created = EmployeeMapping.objects.get_or_create(workspace=self.workspace,
                                                                              employee_email=employee_email)
            employee_mapping.contact_name = contact_name
            employee_mapping.save()
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
            return self.update(request, *args, **kwargs)
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
            self.workspace.transform_sql = request.POST.get('transform_sql')
            self.workspace.save()
        return HttpResponseRedirect(self.request.path_info)

    def update(self, request, workspace_id):
        self.form.fields['transform_sql'].widget.attrs['disabled'] = False
        self.context['save_button'] = True
        return render(request, self.template_name, self.context)


class ScheduleView(View):
    """
    Schedule View
    """
    template_name = "xero_workspace/schedule.html"

    def get(self, request, workspace_id):
        workspace = Workspace.objects.get(id=workspace_id)
        schedule = WorkspaceSchedule.objects.get(workspace__id=workspace_id).schedule
        form = ScheduleForm(initial={'minutes': schedule.minutes})
        form.fields['next_run'].widget.js_options['defaultDate'] = schedule.next_run.strftime(
            '%Y-%m-%d %I:%M %p')
        context = {"schedule": "active", "workspace_id": workspace_id,
                   "workspace_name": workspace.name, "form": form,
                   "enabled": schedule.repeats}
        return render(request, self.template_name, context)

    def post(self, request, workspace_id):
        schedule = WorkspaceSchedule.objects.get(workspace__id=workspace_id).schedule
        datetime_str = request.POST.get('next_run')
        datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d %I:%M %p')
        minutes = request.POST.get('minutes')
        value = request.POST.get('schedule')
        schedule_enabled = 0
        if value == 'enabled':
            schedule_enabled = -1
        schedule.minutes = minutes
        schedule.next_run = make_aware(datetime_object)
        schedule.repeats = schedule_enabled
        schedule.save()

        return HttpResponseRedirect(self.request.path_info)
