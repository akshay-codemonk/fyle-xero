from fylesdk import FyleSDK

from apps.xero_workspace.models import FyleCredential, Workspace
from fyle_xero_integration_web_app.settings import FYLE_BASE_URL, FYLE_CLIENT_ID, FYLE_CLIENT_SECRET


def connect_to_fyle(workspace_id):
    """
    Returns verified instance of Fyle object that can invoke API calls
    :param workspace_id:
    :return:
    """
    refresh_token = FyleCredential.objects.get(workspace__id=workspace_id).fyle_auth.refresh_token
    connection = FyleSDK(
        base_url=FYLE_BASE_URL,
        client_id=FYLE_CLIENT_ID,
        client_secret=FYLE_CLIENT_SECRET,
        refresh_token=refresh_token
    )
    return connection


def transform(conn, workspace_id):
    """
    Transforms the collected fyle data and mapping data into Xero data
    :param conn:
    :param workspace_id:
    :return:
    """
    qry = Workspace.objects.get(id=workspace_id).transform_sql
    cur = conn.cursor()
    cur.executescript(qry)
    cur.close()
    conn.commit()


def upload_sqlite(file_name, file, connection):
    """
    Uploads sqlite file to AWS using Fyle SDK
    :param file_name: Name of the file to be uploaded
    :param file: file object
    :param connection: Fyle connection
    :return: file_id
    """
    file_id = connection.Files.post(file_name)['id']
    s3_upload_url = connection.Files.create_upload_url(file_id)['url']
    connection.Files.upload_file_to_aws('application/x-sqlite3', file, s3_upload_url)
    return file_id
