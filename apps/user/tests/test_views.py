from django.contrib.auth import get_user_model
from django.test import TestCase


class UserLoginViewTestCases(TestCase):
    """
    Test cases for user login
    """

    def test_login(self):
        user = get_user_model()
        user.objects.create_user(email='user@test.com', password='foo')
        self.client.login(email='user@test.com', password='foo')
        response = self.client.get('/workspace/', follow=True)
        test_user = user.objects.get(email=response.context['user'])
        self.assertEqual(test_user.email, 'user@test.com')
