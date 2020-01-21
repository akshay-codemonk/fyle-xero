from django.test import TestCase

from apps.xero_connect.models import XeroAuth


class XeroAuthTestCases(TestCase):
    """
    Test cases for XeroAuth model
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data
        """
        XeroAuth.objects.create(client_id='12345', client_secret='abcd#1234', refresh_token='qwerty')
        XeroAuth.objects.create(client_id='12345', client_secret='abcd#1234', refresh_token='qwerty',
                                url='https://a.test.com')

    def test_client_id_value(self):
        """
        Test client_id value
        """
        xero_auth = XeroAuth.objects.get(id=1)
        self.assertEqual(xero_auth.client_id, '12345')

    def test_client_secret_value(self):
        """
        Test client_secret value
        """
        xero_auth = XeroAuth.objects.get(id=1)
        self.assertEqual(xero_auth.client_secret, 'abcd#1234')

    def test_refresh_token_value(self):
        """
        Test refresh_token value
        """
        xero_auth = XeroAuth.objects.get(id=1)
        self.assertEqual(xero_auth.refresh_token, 'qwerty')

    def test_default_url_value(self):
        """
        Test default url value
        """
        xero_auth = XeroAuth.objects.get(id=1)
        self.assertEqual(xero_auth.url, 'https://api.xero.com')

    def test_url_value(self):
        """
        Test url value
        """
        xero_auth = XeroAuth.objects.get(id=2)
        self.assertEqual(xero_auth.url, 'https://a.test.com')

    def test_string_representation(self):
        """
        Test model string representation
        """
        xero_auth = XeroAuth.objects.get(id=1)
        self.assertEqual(str(xero_auth), '1')
