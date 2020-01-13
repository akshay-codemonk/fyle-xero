from django.contrib import admin

from apps.xero_workspace.models import Workspace, FyleCredential, WorkspaceSchedule, \
    XeroCredential, CategoryMapping, EmployeeMapping, Activity, ProjectMapping, \
    Invoice, InvoiceLineItem


class WorkspaceAdmin(admin.ModelAdmin):
    """
    Admin options for Workspace Model
    """
    list_display = ('name', 'id', 'created_at', 'updated_at')
    list_filter = ['created_at', 'updated_at']


class XeroCredentialAdmin(admin.ModelAdmin):
    """
    Admin options for XeroCredential Model
    """
    list_display = ('id', 'created_at', 'updated_at')
    list_filter = ['created_at', 'updated_at']


class FyleCredentialAdmin(admin.ModelAdmin):
    """
    Admin options FyleCredential Model
    """
    list_display = ('id', 'created_at', 'updated_at')
    list_filter = ['created_at', 'updated_at']


class WorkspaceScheduleAdmin(admin.ModelAdmin):
    """
    Admin options WorkspaceSchedule Model
    """
    list_display = ('id', 'workspace', 'schedule', 'created_at', 'updated_at')
    list_filter = ['workspace', 'schedule', 'created_at', 'updated_at']


class EmployeeMappingAdmin(admin.ModelAdmin):
    """
    Admin options EmployeeMapping Model
    """
    list_display = ('workspace', 'id', 'employee_email', 'contact_name', 'created_at', 'updated_at')
    list_filter = ['workspace', 'created_at', 'updated_at']


class CategoryMappingAdmin(admin.ModelAdmin):
    """
    Admin options CategoryMapping Model
    """
    list_display = ('workspace', 'id', 'category', 'sub_category', 'account_code', 'created_at', 'updated_at')
    list_filter = ['workspace', 'created_at', 'updated_at']


class ProjectMappingAdmin(admin.ModelAdmin):
    """
    Admin options CategoryMapping Model
    """
    list_display = ('workspace', 'id', 'project_name', 'tracking_category_name',
                    'tracking_category_option', 'created_at', 'updated_at')
    list_filter = ['workspace', 'created_at', 'updated_at']


class ActivityAdmin(admin.ModelAdmin):
    """
    Admin options for Activity Model
    """
    list_display = ('id', 'status', 'triggered_by', 'created_at', 'updated_at')
    list_filter = ['status', 'triggered_by', 'created_at', 'updated_at']


class InvoiceAdmin(admin.ModelAdmin):
    """
    Admin options for Invoice Model
    """
    list_display = ('invoice_number', 'invoice_id', 'contact_name', 'date',
                    'due_date', 'created_at', 'updated_at')
    list_filter = ['invoice_number', 'date', 'created_at', 'updated_at']


class InvoiceLineItemAdmin(admin.ModelAdmin):
    """
    Admin options for InvoiceLineItem Model
    """
    list_display = ('id', 'account_name', 'account_code', 'amount',
                    'created_at', 'updated_at')
    list_filter = ['account_code', 'account_name', 'created_at', 'updated_at']


# Register Models with Admin
admin.site.register(Workspace, WorkspaceAdmin)
admin.site.register(XeroCredential, XeroCredentialAdmin)
admin.site.register(FyleCredential, FyleCredentialAdmin)
admin.site.register(WorkspaceSchedule, WorkspaceScheduleAdmin)
admin.site.register(EmployeeMapping, EmployeeMappingAdmin)
admin.site.register(CategoryMapping, CategoryMappingAdmin)
admin.site.register(ProjectMapping, ProjectMappingAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceLineItem, InvoiceLineItemAdmin)
