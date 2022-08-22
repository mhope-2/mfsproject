import requests
import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import QuotationItems, Quotations
from .serializers import QuotationItemsSerializer, QuotationSerializer
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
class QuotationsViewSet(viewsets.GenericViewSet):

    serializer_class = QuotationSerializer

    def list(self, request): 
        try:
            quotation = Quotations.objects.filter(deleted_at=None)
            serializer = QuotationSerializer(quotation, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def create(self, request): 
        try:
            quotation = request.data["quotation"]
            quotation_items = request.data["quotation_items"]

            # make request to product service to get user's data
            try:
                user_data = requests.get(f"http://localhost:8000/api/v1/product/service/user/{quotation['user_id']}/retrieve").json()
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

            quotation["issued_by"] = str(user_data["first_name"]) + " " + str(user_data["last_name"])

            # generate quotation number
            quotation["quotation_no"] = self.create_quotation_no()
            quotation_serializer = QuotationSerializer(data=quotation)
            quotation_serializer.is_valid(raise_exception=True)
            quotation_serializer.save()
            
            # quotation items
            saved_quotation_booking_code = str(Quotations.objects.last())
            for item in quotation_items:
                item["quotation_no"] = saved_quotation_booking_code
                quotation_item_serializer = QuotationItemsSerializer(data=item)
                quotation_item_serializer.is_valid(raise_exception=True)
                quotation_item_serializer.save()

            return Response({"quotation": quotation, "quotation_items": quotation_items}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error("Error: {}".format(str(e)))
            return Response({"error: ":str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @transaction.atomic
    def retrieve(self, request, pk=None): 
        try:
           # get quotation data
            quot_data = QuotationSerializer(Quotations.objects.get(id=pk)).data

            # get inv creator
            quotation_items_list = []

            quotation_items = QuotationItemsSerializer(QuotationItems.objects.filter(quotation_no=quot_data['quotation_no']), many=True).data
            for item in quotation_items:

                # get product data via API call
                try:
                    product_data = requests.get(f"http://localhost:8000/api/v1/product/service/product/{item['product_id']}/retrieve").json()
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

                item["product_details"] = product_data
                quotation_items_list.append(item)
                
            return Response({"quotation": quot_data, "quotation_items": quotation_items_list,
            "message": "Quotation sucessfully retrieved"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_404_NOT_FOUND)


    @transaction.atomic
    def update(self, request, pk=None): 
        try:
            # updating quotation
            quotation = Quotations.objects.get(id=pk)
            quotation_items = QuotationItems.objects.filter(quotation_no=quotation.quotation_no)

            quotation_serializer = QuotationSerializer(instance=quotation, data=request.data["quotation"])
            quotation_serializer.is_valid(raise_exception=True)
            quotation_serializer.save()

            # updating quotation items
            for index,item in enumerate(quotation_items):
                quotation_item_serializer = QuotationItemsSerializer(instance = item, data=request.data["quotation_items"][index])
                quotation_item_serializer.is_valid(raise_exception=True)
                quotation_item_serializer.save()

                return Response(request.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_404_NOT_FOUND)

    @transaction.atomic
    def destroy(self, request, pk=None):
        try:
            quotation = Quotations.objects.get(id=pk)
            quotation.delete()
            return Response({"response":"Quotation deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_404_NOT_FOUND)


    # generate sequential quotation numbers
    def create_quotation_no(self):
        try:
            # check for latest quotation number
            logger.debug("last quot no: {}".format(str(Quotations.objects.latest('created_at'))))
            latest_quotation_no = int(str(Quotations.objects.latest('created_at')).strip("QUOT"))
            quotation_no = "QUOT" + str(latest_quotation_no + 1)
            logger.debug("generated quotation no: {}".format(quotation_no))
        except Exception as e:
            latest_quotation_no = 0
            quotation_no = str("QUOT" + str(latest_quotation_no + 1))
        
        return quotation_no
