from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch

class UserRegistrationTestCase(APITestCase):
    @patch('core.serializers.UserRegistrationSerializer.save')
    def test_register_user(self, mock_save):
        # Mock the save method so it doesn't actually save the user in the database
        mock_save.return_value = True  # Simulate the user being saved successfully

        url = reverse('register_user')  # URL for the register_user view
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'securepassword123'
        }

        response = self.client.post(url, data, format='json')

        # Check if the response is successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User created successfully!')

        mock_save.assert_called_once()  # Ensures that the save method was called
