from django.test import TestCase

from apps.fyle_connect.models import FyleAuth


class FyleAuthTestCases(TestCase):
    """
    Test cases for FyleAuth model
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data
        """
        FyleAuth.objects.create(client_id='12345', client_secret='abcd#1234', refresh_token='qwerty')
        FyleAuth.objects.create(client_id='12345', client_secret='abcd#1234', refresh_token='qwerty',
                                url='https://a.test.com')

    def test_client_id_value(self):
        """
        Test client_id value
        """
        fyle_auth = FyleAuth.objects.get(id=1)
        self.assertEqual(fyle_auth.client_id, '12345')

    def test_client_secret_value(self):
        """
        Test client_secret value
        """
        fyle_auth = FyleAuth.objects.get(id=1)
        self.assertEqual(fyle_auth.client_secret, 'abcd#1234')

    def test_refresh_token_value(self):
        """
        Test refresh_token value
        """
        fyle_auth = FyleAuth.objects.get(id=1)
        self.assertEqual(fyle_auth.refresh_token, 'qwerty')

    def test_default_url_value(self):
        """
        Test default url value
        """
        fyle_auth = FyleAuth.objects.get(id=1)
        self.assertEqual(fyle_auth.url, 'https://app.fyle.in')

    def test_url_value(self):
        """
        Test url value
        """
        fyle_auth = FyleAuth.objects.get(id=2)
        self.assertEqual(fyle_auth.url, 'https://a.test.com')
