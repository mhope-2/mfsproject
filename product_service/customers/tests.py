# from django.test import TestCase
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from .models import Customer

# class CustomerTests(APITestCase):
    # def test_retrieve_customer(self):
    #     """
    #     Ensure we can retrieve a new customer object.
    #     """
    #     url = reverse('customer-retrieve'+"/13")
    #     # data = {'name': 'DabApps'}
    #     response = self.client.get(url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Customer.objects.count(), 1)
    #     self.assertEqual(Customer.objects.get().name, 'DabApps')

    # def test_fancy(self):
    #     self.assertEqual(1, 1)
