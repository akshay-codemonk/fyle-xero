from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersModelTestCases(TestCase):
    """
    Test cases for the custom User model
    """

    def test_create_user(self):
        """
        Test user creation
        """
        user = get_user_model()
        normal_user = user.objects.create_user(email='user@test.com', password='foo')
        self.assertEqual(normal_user.email, 'user@test.com')
        self.assertTrue(normal_user.is_active)
        self.assertFalse(normal_user.is_staff)
        self.assertFalse(normal_user.is_superuser)
        with self.assertRaises(TypeError):
            user.objects.create_user()
        with self.assertRaises(TypeError):
            user.objects.create_user(email='')
        with self.assertRaises(ValueError):
            user.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        """
        Test superuser creation
        """
        user = get_user_model()
        admin_user = user.objects.create_superuser('admin@test.com', 'foo')
        self.assertEqual(admin_user.email, 'admin@test.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
