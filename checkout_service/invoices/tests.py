from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Invoices
from quotations.tests import QuotationTests
from rest_framework import status


class invoiceTests(APITestCase):

    """
    Test cases for the Invoices model and its operations.
    It depends on a running product service instance.
    """

    def setUp(self):

        self.valid_payload = {
            "invoice": {
                "invoice_no": "INV1",
                "quotation_no": "QUOT1",
                "user_id": 1,
                "customer_id": 1,
                "customer_first_name":"Sam",
                "customer_middle_name":"",
                "customer_last_name":"Kay",
                "customer_phone":"0556581926",
                "customer_email":"mfsuser@gmail.com",
                "net_total": 70.00,
                "amount_received": 70.00,
                "cash": 40.00,
                "mobile_money": 30.00,
                "bank_transfer": 10.00,
                "issued_by":"John Doe"
            },
            "invoice_items":[
                {
                    "invoice_id": 1,
                    "invoice_no": "INV1",
                    "product_id":1,
                    "quantity":3,
                    "unit_price": 10.00,
                    "sub_total": 30.00
                },
                {
                    "invoice_id": 1,
                    "invoice_no": "INV1",
                    "product_id":2,
                    "quantity":2,
                    "unit_price": 20.00,
                    "sub_total": 40.00
                }
            ]
        }
        

        self.invalid_payload = {
            "invoice": {
                "invoice_no": "INV1",
                "quotation_no": "QUOT1",
                "user_id": 1,
                "customer_id": 1,
                "customer_first_name":"Sam",
                "customer_middle_name":"",
                "customer_phone":"0556581926",
                "customer_email":"mfsuser@gmail.com",
                "amount_received": 70.00,
                "cash": 40.00,
                "mobile_money": 30.00,
                "bank_transfer": 10.00,
                "issued_by":"John Doe"
            },
            "invoice_items":[
                {
                    "invoice_id": 1,
                    "invoice_no": "INV1",
                    "quantity":3,
                    "unit_price": 10.00,
                    "sub_total": 30.00
                },
                {
                    "invoice_id": 1,
                    "invoice_no": "INV1",
                    "product_id":2,
                    "quantity":2,
                    "unit_price": 20.00,
                    "sub_total": 40.00
                }
            ]
        }
    def test_create_invoice(self):
        """
        Ensure we can create a new invoice and retrieve the data.
        """

        response = self.client.post(reverse('create-invoice'), self.valid_payload, secure=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoices.objects.count(), 1)

    def test_create_invalid_invoice(self):
        """
        Ensure we can't create a new Invoices with invalid payload.
        """
        response = self.client.post(reverse('create-invoice'), self.invalid_payload, secure=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('retrieve-invoice', args=[1]), secure=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_retrieve_invoice(self):
        """
        Ensure we can create a new Invoices and retrieve the data.
        """
        self.test_create_invoice()

        response = self.client.get(reverse('retrieve-invoice', args=[1]), secure=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Invoices.objects.count(), 1)
    
    def test_retrieve_invalid_invoice(self):
        """
        Ensure we can create a new invoice and retrieve the data.
        """
        self.test_create_invoice()

        response = self.client.get(reverse('retrieve-invoice', args=[5]), secure=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def tearDown(self) -> None:
        return super().tearDown()

