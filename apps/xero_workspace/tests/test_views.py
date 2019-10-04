from django.test import TestCase, Client
from django.urls import reverse

from apps.user.models import UserProfile
from apps.xero_workspace.models import Workspace


class WorkspaceViewTest(TestCase):
    """
    Test cases for Workspace view
    """

    def setUp(self):
        """
        Setup sample data for testing
        """
        user1 = UserProfile.objects.create_user(email="user1@test.com", password="foo")
        user2 = UserProfile.objects.create_user(email="user2@test.com", password="bar")
        workspace1 = Workspace.objects.create(name="test workspace 1")
        workspace2 = Workspace.objects.create(name="test workspace 2")
        workspace1.user.add(user1)
        workspace2.user.add(user2)
        self.client.login(email='user1@test.com', password='foo')

    def test_view_url_exists_at_desired_location(self):
        """
        Test fetching the workspace dashboard
        """
        response = self.client.get('/workspace/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """
        Test if the url is accessible by name
        """
        response = self.client.get(reverse('xero_workspace:workspace'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Test for the template used in workspace dashboard
        """
        response = self.client.get(reverse('xero_workspace:workspace'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'xero_workspace/workspace.html')

    def test_get_user_workspaces(self):
        """
        Test fetching user workspaces
        """
        response = self.client.get('/workspace/', follow=True)
        workspace = Workspace.objects.get(name='test workspace 1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['workspaces']) == 1)
        self.assertEqual(response.context['workspaces'][0].name, workspace.name)

    def test_create_workspaces(self):
        """
        Test creation of workspace
        """
        client = Client()
        response = client.post('/workspace/', kwargs={'name': 'test workspace 3'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/?next=/workspace/', status_code=302, target_status_code=200)
