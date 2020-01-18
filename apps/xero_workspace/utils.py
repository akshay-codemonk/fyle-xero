from fylesdk import FyleSDK
from xerosdk import XeroSDK

from apps.xero_workspace.models import FyleCredential, XeroCredential
from fyle_xero_integration_web_app.settings import FYLE_BASE_URL, FYLE_CLIENT_ID, FYLE_CLIENT_SECRET, \
    XERO_BASE_URL, XERO_CLIENT_ID, XERO_CLIENT_SECRET


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


def connect_to_xero(workspace_id):
    """
    Returns verified instance of Xero object that can invoke API calls
    :param workspace_id
    :return connection: XeroSDK object
    """

    xero_auth = XeroCredential.objects.get(workspace__id=workspace_id).xero_auth
    refresh_token = xero_auth.refresh_token
    connection = XeroSDK(
        base_url=XERO_BASE_URL,
        client_id=XERO_CLIENT_ID,
        client_secret=XERO_CLIENT_SECRET,
        refresh_token=refresh_token
    )
    xero_auth.refresh_token = connection.refresh_token
    xero_auth.save()
    return connection
