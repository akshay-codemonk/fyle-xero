from apps.task_log.tasks import fetch_expenses_and_create_groups

from apps.task_log.models import TaskLog
from apps.xero_workspace.utils import connect_to_fyle
from fyle_jobs import FyleJobsSDK
from fyle_xero_integration_web_app import settings


def schedule_sync(workspace_id, schedule, user):
    """
    Schedule sync
    :param workspace_id: workspace_id
    :param schedule: schedule object
    :param user: user email
    """
    fyle_sdk_connection = connect_to_fyle(workspace_id)

    jobs = FyleJobsSDK(settings.FYLE_JOBS_URL, fyle_sdk_connection)

    created_job = jobs.trigger_interval(
        callback_url='{0}{1}'.format(
            settings.API_BASE_URL,
            '/workspace_jobs/{0}/settings/schedule/trigger/'.format(
                workspace_id
            )
        ),
        callback_method='POST',
        object_id=schedule.id,
        job_description='Fetch expenses: Workspace id - {0}, user - {1}'.format(
            workspace_id, user
        ),
        start_datetime=schedule.start_datetime.strftime('%Y-%m-%d %H:%M:00.00'),
        hours=int(schedule.interval_hours)
    )
    schedule.fyle_job_id = created_job['id']
    schedule.save()


def run_sync_schedule(workspace_id, user):
    """
    Run sync schedule
    :param workspace_id: workspace id
    :param user: user email
    """
    task_log = TaskLog.objects.create(
        workspace_id=workspace_id,
        type="FETCHING EXPENSES",
        status="IN_PROGRESS"
    )

    fetch_expenses_and_create_groups(
        workspace_id=workspace_id,
        task_log=task_log,
        user=user
    )
