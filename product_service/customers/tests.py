from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from customers.models import Customer
from rest_framework import status


class CustomerTests(APITestCase):

    """
    Test cases for the Customer model and its operations.
    """

    def setUp(self):

        self.valid_payload = {
            "first_name": "Sam",
            "middle_name": "",
            "last_name": "Kay",
            "phone": "0556581926",
            "email": "mfsuser@gmail.com",
            "address": "1 Cresecent Road",
        }

        # username field omitted
        self.invalid_payload = {
            "middle_name": "",
            "last_name": "Kay",
            "phone": "0556581926",
            "email": "mfsuser@gmail.com",
            "address": "1 Cresecent Road",
        }

    def test_create_and_retrieve_customer(self):
        """
        Ensure we can create a new customer and retrieve the data.
        """
        response = self.client.post(
            reverse("create-customer"), self.valid_payload, secure=True, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Customer.objects.get().first_name, "Sam")

    def test_create_invalid_customer(self):
        """
        Ensure we can't create a new customer with invalid payload.
        """
        response = self.client.post(
            reverse("create-customer"), self.invalid_payload, secure=True, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Customer.objects.count(), 0)

        response = self.client.get(
            reverse("retrieve-customer", args=[1]), secure=True, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Customer.objects.count(), 0)

    def test_retrieve_customer(self):
        """
        Ensure we can create a new customer and retrieve the data.
        """
        self.test_create_and_retrieve_customer()

        response = self.client.get(
            reverse("retrieve-customer", args=[1]), secure=True, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Customer.objects.get().first_name, "Sam")

    def test_retrieve_invalid_customer(self):
        """
        Ensure we can create a new customer and retrieve the data.
        """
        self.test_create_and_retrieve_customer()

        response = self.client.get(
            reverse("retrieve-customer", args=[5]), secure=True, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_customer(self):
        """
        Ensure we can update a customer.
        """
        self.test_create_and_retrieve_customer()

        response = self.client.put(
            reverse("update-customer", args=[1]),
            self.valid_payload,
            secure=True,
            format="json",
        )
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Customer.objects.get().first_name, "Sam")

    def test_update_invalid_customer(self):
        """
        Ensure we can't update a customer with invalid id.
        """
        response = self.client.put(
            reverse("update-customer", args=[5]),
            self.valid_payload,
            secure=True,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Customer.objects.count(), 0)

    def test_delete_customer(self):
        """
        Ensure we can delete a customer.
        """
        self.test_create_and_retrieve_customer()

        response = self.client.delete(
            reverse("delete-customer", args=[1]), secure=True, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Customer.objects.count(), 0)

    def test_delete_invalid_customer(self):
        """
        Ensure we can't delete a customer with invalid id.
        """
        response = self.client.delete(
            reverse("delete-customer", args=[5]), secure=True, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Customer.objects.count(), 0)

    def tearDown(self) -> None:
        return super().tearDown()
