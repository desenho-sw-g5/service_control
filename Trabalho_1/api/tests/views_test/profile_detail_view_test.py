import json

from django.test import TestCase

from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from rest_framework import status
from rest_framework.authtoken.models import Token

from core.models import Profile, User

from api.views import ProfileDetail
from api.serializers import UserSerializer


class ProfileDetailViewTestCase(TestCase):
    """Test suite for the api profile list view."""

    def setUp(self):
        """Define the test global variables."""
        if not User.objects.filter(username='testadmin').exists():
            self.admin_user = User.objects.create_superuser(username='testadmin', password='123', email='')
            Token.objects.create(user=self.admin_user)

        user = User.objects.create(username='testuser1', email='test@user1.com', password='sometestpass')
        self.test_profile = Profile.objects.create(user=user)

        self.factory = APIRequestFactory()
        self.view = ProfileDetail.as_view()


    def test_dont_get_profile_data_without_authorization(self):
        """Test dont get profile data without authorization"""
        request = self.factory.get('/core/api/profile/')
        response = self.view(request, pk=self.test_profile.id)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_data(self):
        """Test get profile data"""
        request = self.factory.get('/core/api/profile/')
        force_authenticate(request, user=self.admin_user, token=self.admin_user.auth_token)
        response = self.view(request, pk=self.test_profile.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('user' in response.data)

    def test_update_profile_data(self):
        """Test update profile data"""

        new_email = 'just@some.test'
        data = json.dumps({'user': {'email': new_email}})

        request = self.factory.patch('/core/api/profile/',
                                    data=data,
                                    content_type='application/json')

        force_authenticate(request, user=self.admin_user, token=self.admin_user.auth_token)
        response = self.view(request, pk=self.test_profile.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('user' in response.data)
        self.assertEqual(response.data['user']['email'], new_email)

    def test_delete_profile(self):
        """Test delete profile"""

        request = self.factory.delete('/core/api/profile/',
                                    content_type='application/json')

        force_authenticate(request, user=self.admin_user, token=self.admin_user.auth_token)
        response = self.view(request, pk=self.test_profile.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Profile.objects.filter(pk=self.test_profile.id).exists())
