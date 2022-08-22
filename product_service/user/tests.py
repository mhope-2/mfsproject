from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User
from rest_framework import status


class UserTests(APITestCase):

    """
    Test cases for the User model and its operations.
    """

    def setUp(self):

        self.valid_payload = {
            "username": "sam",
            "password": "sampassword927",
            "first_name": "Sam",
            "middle_name": "",
            "last_name": "Kay",
            "phone": "0556581926",
            "email": "mfsuser@gmail.com",
            "gender": "Male",
        }

        # username field omitted
        self.invalid_payload = {
            # "username": "sam",
            "password": "sampassword927",
            "first_name": "Sam",
            "middle_name": "",
            "last_name": "Kay",
            "phone": "0556581926",
            "email": "mfsuser@gmail.com",
            "gender": "Male",
        }

    def test_create_and_retrieve_user(self):
        """
        Ensure we can create a new User and retrieve the data.
        """
        response = self.client.post(
            reverse("create-user"), self.valid_payload, secure=True, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().first_name, "Sam")

    def test_create_invalid_user(self):
        """
        Ensure we can't create a new User with invalid payload.
        """
        response = self.client.post(
            reverse("create-user"), self.invalid_payload, secure=True, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

        response = self.client.get(
            reverse("retrieve-user", args=[1]), secure=True, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(User.objects.count(), 0)

    def test_retrieve_user(self):
        """
        Ensure we can create a new User and retrieve the data.
        """
        self.test_create_and_retrieve_user()

        response = self.client.get(
            reverse("retrieve-user", args=[1]), secure=True, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().first_name, "Sam")

    def test_retrieve_invalid_user(self):
        """
        Ensure we can create a new User and retrieve the data.
        """
        self.test_create_and_retrieve_user()

        response = self.client.get(
            reverse("retrieve-user", args=[5]), secure=True, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user(self):
        """
        Ensure we can update a User.
        """
        self.test_create_and_retrieve_user()

        response = self.client.put(
            reverse("update-user", args=[1]),
            self.valid_payload,
            secure=True,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().first_name, "Sam")

    def test_update_invalid_User(self):
        """
        Ensure we can't update a User with invalid id.
        """

        response = self.client.put(
            reverse("update-user", args=[5]),
            self.valid_payload,
            secure=True,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(User.objects.count(), 0)

    def test_delete_user(self):
        """
        Ensure we can delete a User.
        """
        self.test_create_and_retrieve_user()

        response = self.client.delete(
            reverse("delete-user", args=[1]), secure=True, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 0)

    def test_delete_invalid_User(self):
        """
        Ensure we can't delete a User with invalid id.
        """
        response = self.client.delete(
            reverse("delete-user", args=[5]), secure=True, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(User.objects.count(), 0)

    def tearDown(self) -> None:
        return super().tearDown()
