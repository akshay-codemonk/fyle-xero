import sqlite3

import requests
from fylesdk import NoPrivilegeError
from xero.exceptions import XeroUnauthorized

from apps.fyle_connect.utils import extract_fyle
from apps.sync_activity.models import Activity
from apps.sync_activity.utils import upload_sqlite, update_activity_status
from apps.xero_workspace.models import XeroCredential, FyleCredential, Workspace, WorkspaceActivity
from apps.xero_workspace.utils import connect_to_xero, connect_to_fyle, generate_invoice_request_data, create_invoice, \
    load_mapping, transform


def sync_xero(workspace_id, activity_id):
    """
    Synchronise data from Fyle to Xero
    :param workspace_id:
    :param activity_id:
    :return:
    """
    sqlite_file_path = f'/tmp/{workspace_id}_{activity_id}.db'
    conn = sqlite3.connect(sqlite_file_path)
    activity = Activity.objects.get(id=activity_id)

    try:
        fyle_connection = connect_to_fyle(workspace_id)
        xero = connect_to_xero(workspace_id)

        load_mapping(workspace_id, conn, xero)

        bills_exist = extract_fyle(fyle_connection, conn)

        if bills_exist:
            transform(conn, workspace_id)
            data = generate_invoice_request_data(conn)
            activity.request_data = data
            activity.save()
            created_records = create_invoice(data, xero)
            activity.response_data = created_records
            activity.save()
            # load_exports_to_fyle()
        conn.close()

        with open(sqlite_file_path, "rb") as file:
            file_content = file.read()
        file_id = upload_sqlite(f'{workspace_id}_{activity_id}.db', file_content, fyle_connection)
        activity.sync_db_file_id = file_id

        update_activity_status(activity, 'Synchronisation completed successfully', Activity.STATUS.success)

    except FyleCredential.DoesNotExist:
        update_activity_status(activity, 'Please connect your Source (Fyle) Account', Activity.STATUS.failed)

    except XeroCredential.DoesNotExist:
        update_activity_status(activity, 'Please connect your Destination (Xero) Account', Activity.STATUS.failed)

    except XeroUnauthorized as error:
        update_activity_status(activity, f'Unable to connect to your Xero account, {error}', Activity.STATUS.failed)

    except sqlite3.OperationalError as error:
        update_activity_status(activity, f'Error performing transform operation, {error}', Activity.STATUS.failed)

    except requests.exceptions.ConnectionError:
        update_activity_status(activity, 'Failed to establish a network connection, please try again later',
                               Activity.STATUS.timeout)

    except NoPrivilegeError as error:
        update_activity_status(activity, f'Please check your Fyle credentials, {error}', Activity.STATUS.failed)

    except KeyError as error:
        update_activity_status(activity, f'Please check your mapping tables, {error}', Activity.STATUS.failed)

    finally:
        if activity.status == Activity.STATUS.in_progress:
            update_activity_status(activity_id, 'An error occurred while processing your request',
                                   Activity.STATUS.failed)
        conn.close()


def sync_xero_scheduled(workspace_id):
    workspace = Workspace.objects.get(id=workspace_id)
    activity = Activity.objects.create(transform_sql=workspace.transform_sql,
                                       error_msg='Synchronisation in progress')
    activity_id = activity.id
    WorkspaceActivity.objects.create(workspace=workspace, activity=activity)
    sync_xero(workspace_id, activity_id)
