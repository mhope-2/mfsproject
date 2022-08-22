from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Quotations
from rest_framework import status


class QuotationTests(APITestCase):

    """
    Test cases for the Quotations model and its operations.
    It depends on a running product service instance
    """

    def setUp(self):

        self.valid_payload = {
            "quotation": {
                "quotation_no": "QUOT1",
                "user_id": 1,
                "customer_id": 1,
                "customer_first_name":"Sam",
                "customer_middle_name":"",
                "customer_last_name":"Kay",
                "customer_phone":"0556581926",
                "customer_email":"mfsuser@gmail.com",
                "issued_by":"John Doe",
            },
            "quotation_items":[
                {
                    "product_id":1,
                    "quantity":3,
                    "quotation_no": "QUOT1"
                },
                {
                    "product_id":2,
                    "quantity":3,
                    "quotation_no": "QUOT1"
                }
            ]
        }
        
        self.invalid_payload = {
           "quotation": {
                "id": "",
                "user_id": 1,
                "customer_id": 1,
                "customer_first_name":"Sam",
                "customer_middle_name":"",
                "customer_phone":"0556581926",
                "customer_email":"mfsuser@gmail.com",
            },
            "quotation_items":[
                {
                    "product_id":1,
                    "quantity":3
                },
                {
                    "product_id":2,
                    "quantity":3
                }
            ]
        }

    def test_create_quotation(self):
        """
        Ensure we can create a new Quotation and retrieve the data.
        """

        response = self.client.post(reverse('create-quotation'), self.valid_payload, secure=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quotations.objects.count(), 1)

    def test_create_invalid_quotation(self):
        """
        Ensure we can't create a new Quotations with invalid payload.
        """
        response = self.client.post(reverse('create-quotation'), self.invalid_payload, secure=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Quotations.objects.count(), 0)

        response = self.client.get(reverse('retrieve-quotation', args=[1]), secure=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Quotations.objects.count(), 0)


    def test_retrieve_quotation(self):
        """
        Ensure we can create a new Quotations and retrieve the data.
        """
        self.test_create_quotation()

        response = self.client.get(reverse('retrieve-quotation', args=[1]), secure=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Quotations.objects.count(), 1)
    
    def test_retrieve_invalid_quotation(self):
        """
        Ensure we can create a new Quotation and retrieve the data.
        """
        self.test_create_quotation()

        response = self.client.get(reverse('retrieve-quotation', args=[5]), secure=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_update_quotation(self):
        """
        Ensure we can update a Quotation
        """
        self.test_create_quotation()

        response = self.client.put(reverse('update-quotation', args=[1]), self.valid_payload, secure=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Quotations.objects.count(), 1)
    
    def test_update_invalid_quotation(self):
        """
        Ensure we can't update a Quotation with invalid id.
        """

        response = self.client.put(reverse('update-quotation', args=[5]), self.valid_payload, secure=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Quotations.objects.count(), 0)

    def test_delete_quotation(self):
        """
        Ensure we can delete a Quotations.
        """
        self.test_create_quotation()

        response = self.client.delete(reverse('delete-quotation', args=[1]), secure=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Quotations.objects.count(), 0)
    
    def test_delete_invalid_quotation(self):
        """
        Ensure we can't delete a Quotation with invalid id.
        """
        response = self.client.delete(reverse('delete-quotation', args=[5]), secure=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Quotations.objects.count(), 0)

    def tearDown(self) -> None:
        return super().tearDown()

