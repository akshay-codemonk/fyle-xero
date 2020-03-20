from django.urls import path, include

from apps.xero_workspace.views import ScheduleSyncView

urlpatterns = [
    path('<int:workspace_id>/expense_group/', include('apps.fyle_expense.job_urls')),
    path('<int:workspace_id>/settings/schedule/trigger/', ScheduleSyncView.as_view(), name="schedule_trigger"),
]
