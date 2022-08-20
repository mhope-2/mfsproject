from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import InvoiceItems, Invoices
from quotations.models import Quotations
from product_service.user.serializers import UserSerializer

from .serializers import InvoiceItemsSerializer, InvoiceSerializer
from product_service.user.models import User
from product_service.products.serializers import ProductsSerializer
from product_service.products.models import Products

from django.db import transaction

from pathlib import Path
# Create your views here.


import logging
logger = logging.getLogger(__name__)


class InvoicesViewSet(viewsets.GenericViewSet):

    @transaction.atomic
    def list(self, request): 
        try:
            invoice = Invoices.objects.filter(deleted_at=None).order_by('-created_at')
            paginated_queryset = self.paginate_queryset(invoice)
            serializer = InvoiceSerializer(paginated_queryset, many=True)
            return self.get_paginated_response(serializer.data)
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
            user_data = User.objects.get(id=invoice["user_id"])
            user_data_serializer = UserSerializer(user_data)

            invoice["issued_by"] = str(user_data_serializer.data["first_name"]) + " " + str(user_data_serializer.data["last_name"])


            # get generated invoice number
            try:
                invoice["invoice_no"] = self.create_invoice_no()
            except Exception as e:
                return Response({"response":"Error creating invoice number"}, status=status.HTTP_400_BAD_REQUEST)

            # check if incoming quotation exists
            if not Quotations.objects.filter(quotation_no=str(invoice['quotation_no'])).exists():
                return Response({"response":"Invalid Quotation Number"}, status=status.HTTP_400_BAD_REQUEST)

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
                # logger.debug(str(invoice_serializer)
            
                # invoice items list
            
            invoice_items_list = []

            for item in invoice_items:

                product = Products.objects.get(id=item["product_id"])
                product_serializer = ProductsSerializer(product)

                item["product_details"] = product_serializer.data

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
            user_data = UserSerializer( User.objects.get(id=invoice_data['user_id']) ).data 
            invoice_items_list = []

            invoice_items = InvoiceItemsSerializer(InvoiceItems.objects.filter(invoice_no=invoice_data['invoice_no']), many=True).data
            for item in invoice_items:
                product = Products.objects.get(id=item["product_id"])
                product_serializer = ProductsSerializer(product)

                item["product_details"] = product_serializer.data
                invoice_items_list.append(item)

            return Response({"invoice": invoice_data, "invoice_items": invoice_items_list,
            "message": "Invoice sucessfully retrieved"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Error retrieving invoice with id {}. Cause: {}".format(pk, str(e)))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)


    @transaction.atomic
    def retrieve(self, request, pk=None):
        try:
            # get invoice data
            invoice_data = InvoiceSerializer(Invoices.objects.get(id=pk)).data

            invoice_items_list = []

            invoice_items = InvoiceItemsSerializer(InvoiceItems.objects.filter(invoice_no=invoice_data['invoice_no']), many=True).data
            for item in invoice_items:
                product = Products.objects.get(id=item["product_id"])
                product_serializer = ProductsSerializer(product)

                item["product_details"] = product_serializer.data
                invoice_items_list.append(item)

            return Response({"invoice": invoice_data, "invoice_items": invoice_items_list,
            "message": "Invoice sucessfully retrieved"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Error retrieving invoice with id {}. Cause: {}".format(pk, str(e)))
            return Response({"response": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def update(self, request, pk=None): 
        try:
            logger.debug("UPDATING INVOICE")
            invoice = Invoices.objects.get(id=pk)
            invoice_items = InvoiceItems.objects.filter(invoice_no=invoice.invoice_no)
            
            logger.debug("SERIALIZING INVOICE OBJECT")
            invoice_serializer = InvoiceSerializer(instance=invoice, data=request.data["invoice"])
            invoice_serializer.is_valid(raise_exception=True)
            invoice_serializer.save()

            # saving invoice items
            logger.debug("UPDATING INVOICE ITEMS")
            for index,item in enumerate(invoice_items):
                invoice_item_serializer = InvoiceItemsSerializer(instance = item, data=request.data["invoice_items"][index])
                invoice_item_serializer.is_valid(raise_exception=True)
                invoice_item_serializer.save()

            return Response({"response": request.data, 
            "message": "Successfully updated invoice details"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e))
            return Response({"response":str(e),
            "message": "Error Updating Invoice Details"}, status=status.HTTP_400_BAD_REQUEST)


    @transaction.atomic
    def destroy(self, request, pk=None):
        try:
            with transaction.atomic():
                invoice = Invoices.objects.get(id=pk)
                invoice.delete()
                return Response({"response":"Invoice deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e))
            return Response({"response":str(e),
            "message": "Error deleting invoice"}, status=status.HTTP_400_BAD_REQUEST)


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
    
