from django.contrib import admin

from apps.xero_workspace.models import Workspace, FyleCredential, WorkspaceActivity, WorkspaceSchedule, \
    XeroCredential, CategoryMapping, EmployeeMapping


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


class WorkspaceActivityAdmin(admin.ModelAdmin):
    """
    Admin options WorkspaceActivity Model
    """
    list_display = ('id', 'workspace', 'activity', 'created_at', 'updated_at')
    list_filter = ['workspace', 'activity', 'created_at', 'updated_at']


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


# Register Models with Admin
admin.site.register(Workspace, WorkspaceAdmin)
admin.site.register(XeroCredential, XeroCredentialAdmin)
admin.site.register(FyleCredential, FyleCredentialAdmin)
admin.site.register(WorkspaceActivity, WorkspaceActivityAdmin)
admin.site.register(WorkspaceSchedule, WorkspaceScheduleAdmin)
admin.site.register(EmployeeMapping, EmployeeMappingAdmin)
admin.site.register(CategoryMapping, CategoryMappingAdmin)
