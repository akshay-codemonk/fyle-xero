from django.urls import path, include

urlpatterns = [
    path('<int:workspace_id>/expense_group/', include('apps.fyle_expense.job_urls')),
]
