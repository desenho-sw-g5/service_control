import json

from django.test import TestCase

from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from rest_framework import status
from rest_framework.authtoken.models import Token

from core.models import Profile, User

from api.views import ProfileList


class ProfileListViewTestCase(TestCase):
    """Test suite for the api profile list view."""

    def setUp(self):
        """Define the test global variables."""
        if not User.objects.filter(username='testadmin').exists():
            self.admin_user = User.objects.create_superuser(username='testadmin', password='123', email='')
            Token.objects.create(user=self.admin_user)

        self.factory = APIRequestFactory()
        self.view = ProfileList.as_view()

    def test_only_get_profiles_if_logged_as_admin(self):
        """Test that only a logged admin can get the profiles"""
        request = self.factory.get('/core/api/profile/')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        force_authenticate(request, user=self.admin_user, token=self.admin_user.auth_token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_a_new_profile(self):
        user_data = {
            'username': 'anewuser',
            'password': 'anewuser',
            'email': 'test@user.com'
        }

        request = self.factory.post('/core/api/profile/',
                        data=json.dumps({'user': user_data}),
                        content_type='application/json')

        force_authenticate(request, user=self.admin_user, token=self.admin_user.auth_token)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
