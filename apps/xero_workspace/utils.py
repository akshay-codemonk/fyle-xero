from fylesdk import FyleSDK
from xero import Xero
from xero.auth import PrivateCredentials

from apps.xero_workspace.models import XeroCredential
from fyle_xero_integration_web_app.settings import FYLE_CLIENT_ID, FYLE_CLIENT_SECRET, FYLE_BASE_URL


def connect_xero_private(workspace_id):
    """
    Returns verified instance of Xero object that can invoke private API calls for a given workspace.
    :param workspace_id: Id of the Xero workspace
    :return: verified instance of Xero object
    """
    xero_credential = XeroCredential.objects.get(id=workspace_id)
    rsa_key_path = xero_credential.pem_file.path
    consumer_key = xero_credential.consumer_key

    with open(rsa_key_path) as keyfile:
        rsa_key = keyfile.read()

    credentials = PrivateCredentials(consumer_key, rsa_key)
    xero = Xero(credentials)
    return xero


def upload_file_to_aws(file, refresh_token):
    """
    Uploads file to AWS S3
    :param: file uploaded from frontend, refresh token of workspace
    for FyleSDK connection
    :return: response from upload
    """
    connection = FyleSDK(
        base_url=FYLE_BASE_URL,
        client_id=FYLE_CLIENT_ID,
        client_secret=FYLE_CLIENT_SECRET,
        refresh_token=refresh_token
    )
    uploaded_file_name = file['pem_file'].name
    file_id = connection.Files.post(uploaded_file_name)['id']
    s3_upload_url = connection.Files.create_upload_url(file_id)['url']
    connection.Files.upload_file_to_aws('application/x-pem-file', file, s3_upload_url)
    return file_id
