"""
xero_workspace app URL Configuration
"""

from django.urls import path, include

from apps.fyle_connect.views import FyleTokenView
from apps.xero_workspace.views import WorkspaceView, XeroConnect, EmployeeMappingView, \
    CategoryMappingView, TransformView

app_name = 'xero_workspace'
urlpatterns = [
    path('', WorkspaceView.as_view(), name="workspace"),
    path('<int:workspace_id>/destination/', XeroConnect.as_view(), name="destination"),
    path('<int:workspace_id>/category_mapping/', CategoryMappingView.as_view(),
         name="category_mapping"),
    path('<int:workspace_id>/employee_mapping/', EmployeeMappingView.as_view(),
         name="employee_mapping"),
    path('<int:workspace_id>/transform/', TransformView.as_view(),
         name="transform"),
    path('<int:workspace_id>/source/', include('apps.fyle_connect.urls')),
    path('<int:workspace_id>/activity/', include('apps.sync_activity.urls')),
    path('<int:workspace_id>/schedule/', include('apps.schedule.urls')),
    # Path for getting the Fyle authorisation code
    path('connect/fyle/', FyleTokenView.as_view(), name="fyle_authorise")
]
