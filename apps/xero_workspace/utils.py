from xero import Xero
from xero.auth import PrivateCredentials

from apps.xero_workspace.models import XeroCredential


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
