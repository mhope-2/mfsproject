from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Products
from rest_framework import status


class ProductTests(APITestCase):

    """
    Test cases for the Products model and its operations.
    """

    def setUp(self):

        self.valid_payload = {
            "name": "valid product",
            "brand": "brand1",
            "unit": "PCS",
            "quantity": 3,
            "barcode": "72047239",
            "unit_price": 100.00,
            "description": "first product",
        }

        self.invalid_payload = {
            "id": "",
            "name": "invalid product",
            "brand": "brand1",
            "unit": "PCS",
            "quantity": -2,
            "barcode": "72047239",
            "unit_price": 100.00,
            "description": "first product",
        }

    def test_create_and_retrieve_product(self):
        """
        Ensure we can create a new Products and retrieve the data.
        """
        response = self.client.post(
            reverse("create-product"), self.valid_payload, secure=True, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Products.objects.count(), 1)
        self.assertEqual(Products.objects.get().name, "valid product")

    def test_create_invalid_product(self):
        """
        Ensure we can't create a new Products with invalid payload.
        """
        response = self.client.post(
            reverse("create-product"), self.invalid_payload, secure=True, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Products.objects.count(), 0)

        response = self.client.get(
            reverse("retrieve-product", kwargs={"pk": 1}), secure=True, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Products.objects.count(), 0)

    def test_retrieve_product(self):
        """
        Ensure we can create a new Products and retrieve the data.
        """
        self.test_create_and_retrieve_product()

        response = self.client.get(
            reverse("retrieve-product", args=[1]), secure=True, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Products.objects.count(), 1)
        self.assertEqual(Products.objects.get().name, "valid product")

    def test_retrieve_invalid_product(self):
        """
        Ensure we can create a new Products and retrieve the data.
        """
        self.test_create_and_retrieve_product()

        response = self.client.get(
            reverse("retrieve-product", args=[5]), secure=True, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_product(self):
        """
        Ensure we can update a Products.
        """
        self.test_create_and_retrieve_product()

        response = self.client.put(
            reverse("update-product", args=[1]),
            self.valid_payload,
            secure=True,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Products.objects.count(), 1)
        self.assertEqual(Products.objects.get().name, "valid product")

    def test_update_invalid_product(self):
        """
        Ensure we can't update a Products with invalid id.
        """

        response = self.client.put(
            reverse("update-product", args=[5]),
            self.valid_payload,
            secure=True,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Products.objects.count(), 0)

    def test_delete_product(self):
        """
        Ensure we can delete a Products.
        """
        self.test_create_and_retrieve_product()

        response = self.client.delete(
            reverse("delete-product", args=[1]), secure=True, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Products.objects.count(), 0)

    def test_delete_invalid_product(self):
        """
        Ensure we can't delete a Products with invalid id.
        """
        response = self.client.delete(
            reverse("delete-product", args=[5]), secure=True, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Products.objects.count(), 0)

    def tearDown(self) -> None:
        return super().tearDown()
