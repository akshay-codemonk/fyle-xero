import json

import requests

from fyle_xero_integration_web_app import settings


class FyleOAuth2():

    def __init__(self):
        """
        initialize from settings
        """
        self.client_id = settings.FYLE_CLIENT_ID
        self.client_secret = settings.FYLE_CLIENT_SECRET
        self.authorise_uri = settings.FYLE_AUTHORISE_URI
        self.callback_uri = settings.FYLE_CALLBACK_URI
        self.token_url = settings.FYLE_TOKEN_URI

    def authorise(self, state):
        """
        Initiates the Fyle OAuth2.0 Authorise flow
        :param state:
        :return:
        """
        authorisation_redirect_url = self.authorise_uri + '?response_type=code&client_id=' + self.client_id + \
                                     '&redirect_uri=' + self.callback_uri + '&scope=read' + '&state=' + state
        return authorisation_redirect_url

    def get_tokens(self, authorization_code):
        """
        Exchange the authorisation_code for access and refresh tokens
        :param authorization_code:
        :return dict containing access_token, refresh_token and expiry:
        """
        # authorization_code = raw_input('code: ')

        data = {'grant_type': 'authorization_code', 'client_id': self.client_id, 'client_secret': self.client_secret,
                'code': authorization_code}
        access_token_response = requests.post(self.token_url, data=data, verify=False, allow_redirects=False)

        tokens = json.loads(access_token_response.text)

        return tokens
