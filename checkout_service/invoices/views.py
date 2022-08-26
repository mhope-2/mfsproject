import requests
import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import InvoiceItems, Invoices
from .serializers import InvoiceItemsSerializer, InvoiceSerializer
from django.db import transaction

from pathlib import Path

ROOT_DIR = Path('__file__').resolve().parent
try:
    logging.basicConfig(filename=f'{ROOT_DIR}/logs/checkout_service.log',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        level=logging.DEBUG)
except FileNotFoundError:
    pass
logger = logging.getLogger(__name__)    


# Create your views here.
class InvoicesViewSet(viewsets.GenericViewSet):

    serializer_class = InvoiceSerializer

    @transaction.atomic
    def list(self, request): 
        try:
            invoices = Invoices.objects.filter(deleted_at=None)
            serializer = InvoiceSerializer(invoices, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def create(self, request): 
        try:
            logger.debug("CREATING AN INVOICE")
            invoice = request.data["invoice"]
            invoice_items = request.data["invoice_items"]

            # check for correct sum
            try:
                logger.debug("CHECK FOR SUM (PAYMENT METHODS) == NET TOTAL")
                if sum([invoice.get('cash'), invoice.get('mobile_money'), invoice.get('bank_transfer')]) < invoice.get('net_total'):
                    return Response({"message": "Sum of payments is less than the net total. Invoice not submitted."}, status=status.HTTP_406_NOT_ACCEPTABLE)
            except Exception as e:
                logger.debug(f"ERROR DURING SUM CHECK: {e}")

            logger.debug("getting user from invoice object")
            # make request to product service to get user's data
            try:
                user_data = requests.get(f"http://localhost:8000/api/v1/product/service/user/{invoice['user_id']}/retrieve").json()
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            invoice["issued_by"] = str(user_data["first_name"]) + " " + str(user_data["last_name"])


            # get generated invoice number
            try:
                invoice["invoice_no"] = self.create_invoice_no()
            except Exception as e:
                return Response({"response":"Error creating invoice number"}, status=status.HTTP_400_BAD_REQUEST)

            # saving invoice
            invoice_serializer = InvoiceSerializer(data=invoice)
            invoice_serializer.is_valid(raise_exception=True)
            invoice_serializer.save()
        
        
            logger.debug("getting last booking code: {}".format(str(Invoices.objects.last())))
            saved_invoice_booking_code = str(Invoices.objects.last())

            logger.debug("getting invoice number from saved invoice model")
            invoice_id = InvoiceSerializer(Invoices.objects.get(invoice_no=saved_invoice_booking_code)).data["id"]

            # saving invoice items
            for item in invoice_items:
                item["invoice_id"] = invoice_id
                item["invoice_no"] = saved_invoice_booking_code
                invoice_item_serializer = InvoiceItemsSerializer(data=item)
                invoice_item_serializer.is_valid(raise_exception=True)
                invoice_item_serializer.save()
            
            # invoice items list
            invoice_items_list = []

            for item in invoice_items:

                # get product data
                try:
                    product_data = requests.get(f"http://localhost:8000/api/v1/product/service/product/{item['product_id']}/retrieve").json()
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

                item["product_details"] = product_data

                logger.debug("APPENDING INVOICE ITEMS TO FINAL LIST")
                invoice_items_list.append(item)

            return Response({"invoice": invoice, "invoice_items": invoice_items_list,
                                "message": "Successfully created invoice"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error("Error creating invoice: {}".format(str(e)))
            return Response({"response":str(e), "message": "Error creating invoice"}, status=status.HTTP_400_BAD_REQUEST)


    @transaction.atomic
    def retrieve(self, request, pk=None):
        try:
            # get invoice data
            invoice_data = InvoiceSerializer(Invoices.objects.get(id=pk)).data

            invoice_items_list = []

            invoice_items = InvoiceItemsSerializer(InvoiceItems.objects.filter(invoice_no=invoice_data['invoice_no']), many=True).data
            for item in invoice_items:
                # get product data
                try:
                    product_data = requests.get(f"http://localhost:8000/api/v1/product/service/product/{item['product_id']}/retrieve").json()
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

                item["product_details"] = product_data
                invoice_items_list.append(item)

            return Response({"invoice": invoice_data, "invoice_items": invoice_items_list,
            "message": "Invoice sucessfully retrieved"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Error retrieving invoice with id {}. Cause: {}".format(pk, str(e)))
            return Response({"response": str(e)}, status=status.HTTP_404_NOT_FOUND)

  
    # generate sequential invoice numbers
    @transaction.atomic
    def create_invoice_no(self):
        try:
            with transaction.atomic():
                # check for latest invoice number
                logger.debug("last invoice no: {}".format(str(Invoices.objects.latest('created_at'))))
                latest_invoice_no = int(str(Invoices.objects.latest('created_at')).strip("INV"))
                invoice_no = "INV" + str(latest_invoice_no + 1)
                logger.info("GENERATED INVOICE NO: {}".format(invoice_no))
        except Exception as e:
            latest_invoice_no = 0
            invoice_no = str("INV" + str(latest_invoice_no + 1))
            logger.info("GENERATED IN NO: {}".format(invoice_no))
        
        return invoice_no
    
