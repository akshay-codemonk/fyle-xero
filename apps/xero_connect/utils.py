import json
from base64 import b64encode

import requests

from fyle_xero_integration_web_app.settings import XERO_CLIENT_ID, XERO_CLIENT_SECRET, \
    XERO_REDIRECT_URI, XERO_SCOPE, XERO_AUTHORIZE_URI, XERO_TOKEN_URI


class XeroOAuth2:

    def __init__(self):
        self.__client_id = XERO_CLIENT_ID
        self.__client_secret = XERO_CLIENT_SECRET
        self.__redirect_uri = XERO_REDIRECT_URI
        self.__scope = XERO_SCOPE
        self.__authorize_uri = XERO_AUTHORIZE_URI
        self.__token_uri = XERO_TOKEN_URI

    def authorize(self, state):
        authorization_redirect_url = self.__authorize_uri + '?response_type=code&client_id=' + self.__client_id + \
                                     '&redirect_uri=' + self.__redirect_uri + '&scope=' + self.__scope + \
                                     '&state=' + state
        return authorization_redirect_url

    def get_tokens(self, authorization_code):
        authorization_header = self.__client_id + ":" + self.__client_secret
        headers = {
            "authorization": "Basic " + str(b64encode(authorization_header.encode("utf-8")), "utf-8"),
        }
        data = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": self.__redirect_uri
        }
        response = requests.post(self.__token_uri, headers=headers, data=data)
        token = json.loads(response.text)
        return token
