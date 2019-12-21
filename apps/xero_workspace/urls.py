"""
xero_workspace app URL Configuration
"""

from django.urls import path, include

from apps.fyle_connect.views import FyleTokenView
from apps.xero_workspace.views import WorkspaceView, XeroConnectView, EmployeeMappingView, \
    CategoryMappingView, TransformView, CategoryMappingBulkUploadView, \
    EmployeeMappingBulkUploadView, XeroDisconnectView, DestinationView, ScheduleView, SyncActivityView, \
    ProjectMappingView, ProjectMappingBulkUploadView

app_name = 'xero_workspace'
urlpatterns = [
    path('', WorkspaceView.as_view(), name="workspace"),
    path('<int:workspace_id>/settings/destination/', DestinationView.as_view(), name="destination"),
    path('<int:workspace_id>/settings/destination/connect/', XeroConnectView.as_view(), name="xero_connect"),
    path('<int:workspace_id>/settings/destination/disconnect/', XeroDisconnectView.as_view(), name="xero_disconnect"),
    path('<int:workspace_id>/mappings/category_mapping/', CategoryMappingView.as_view(),
         name="category_mapping"),
    path('<int:workspace_id>/mappings/category_mapping/upload/', CategoryMappingBulkUploadView.as_view(),
         name="category_mapping_bulk_upload"),
    path('<int:workspace_id>/mappings/employee_mapping/', EmployeeMappingView.as_view(),
         name="employee_mapping"),
    path('<int:workspace_id>/mappings/employee_mapping/upload/', EmployeeMappingBulkUploadView.as_view(),
         name="employee_mapping_bulk_upload"),
    path('<int:workspace_id>/mappings/project_mapping/', ProjectMappingView.as_view(),
         name="project_mapping"),
    path('<int:workspace_id>/mappings/project_mapping/upload/', ProjectMappingBulkUploadView.as_view(),
         name="project_mapping_bulk_upload"),
    path('<int:workspace_id>/settings/transform/', TransformView.as_view(),
         name="transform"),
    path('<int:workspace_id>/settings/source/', include('apps.fyle_connect.urls')),
    path('<int:workspace_id>/activity/', SyncActivityView.as_view(), name="activity"),
    path('<int:workspace_id>/settings/schedule/', ScheduleView.as_view(), name="schedule"),
    path('<int:workspace_id>/expense_groups/', include('apps.fyle_expense.urls')),
    # Path for getting the Fyle authorisation code
    path('connect/fyle/', FyleTokenView.as_view(), name="fyle_authorise")
]
