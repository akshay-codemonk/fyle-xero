from fylesdk import FyleSDK

from fyle_xero_integration_web_app.settings import FYLE_BASE_URL, FYLE_CLIENT_ID, FYLE_CLIENT_SECRET


def upload_sqlite(file_name, file, refresh_token):
    """
    Uploads sqlite file to AWS using Fyle SDK
    :param file_name:
    :param file:
    :param refresh_token:
    :return: file_id
    """
    connection = FyleSDK(
        base_url=FYLE_BASE_URL,
        client_id=FYLE_CLIENT_ID,
        client_secret=FYLE_CLIENT_SECRET,
        refresh_token=refresh_token
    )
    file_id = connection.Files.post(file_name)['id']
    s3_upload_url = connection.Files.create_upload_url(file_id)['url']
    connection.Files.upload_file_to_aws('application/x-sqlite3', file, s3_upload_url)
    return file_id
