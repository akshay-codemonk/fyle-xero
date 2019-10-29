import sqlite3

import requests
from fylesdk import NoPrivilegeError
from xero.exceptions import XeroUnauthorized

from apps.fyle_connect.utils import extract_fyle
from apps.xero_workspace.models import XeroCredential, FyleCredential, Workspace, Activity
from apps.xero_workspace.utils import connect_to_xero, connect_to_fyle, generate_invoice_request_data, create_invoice, \
    load_mapping, transform, upload_sqlite


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

        activity.update_status('Synchronisation completed successfully', Activity.STATUS.success)

    except FyleCredential.DoesNotExist:
        activity.update_status('Please connect your Source (Fyle) Account', Activity.STATUS.failed)

    except XeroCredential.DoesNotExist:
        activity.update_status('Please connect your Destination (Xero) Account', Activity.STATUS.failed)

    except XeroUnauthorized as error:
        activity.update_status(f'Unable to connect to your Xero account, {error}', Activity.STATUS.failed)

    except sqlite3.OperationalError as error:
        activity.update_status(f'Error performing transform operation, {error}', Activity.STATUS.failed)

    except requests.exceptions.ConnectionError:
        activity.update_status('Failed to establish a network connection, please try again later',
                               Activity.STATUS.timeout)

    except NoPrivilegeError as error:
        activity.update_status(f'Please check your Fyle credentials, {error}', Activity.STATUS.failed)

    except KeyError as error:
        activity.update_status(f'Please check your mapping tables, {error}', Activity.STATUS.failed)

    finally:
        if activity.status == Activity.STATUS.in_progress:
            activity.update_status('An error occurred while processing your request',
                                   Activity.STATUS.failed)
        conn.close()


def sync_xero_scheduled(workspace_id):
    workspace = Workspace.objects.get(id=workspace_id)
    activity = Activity.objects.create(workspace=workspace, transform_sql=workspace.transform_sql,
                                       error_msg='Synchronisation in progress')
    activity_id = activity.id
    sync_xero(workspace_id, activity_id)
