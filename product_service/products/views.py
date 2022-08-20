from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction

from .models import Products

from .serializers import ProductsSerializer


from pathlib import Path
# Create your views here.

import logging
logger = logging.getLogger(__name__)

# ROOT_DIR = Path('__file__').resolve().parent

# logger.basicConfig(filename=str(ROOT_DIR)+'/logs/product_service.log',
#                     filemode='a',
#                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                     level=logger.DEBUG)


# Create your views here.

class ProductsViewSet(viewsets.GenericViewSet):
    
    @transaction.atomic
    def list(self, request): 
        try:
            products = Products.objects.filter(deleted_at=None)
            serializer = ProductsSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic      
    def create(self, request): 
        try:
            serializer = ProductsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @transaction.atomic
    def retrieve(self, request, pk=None): 
        try:
            product = Products.objects.filter(id=pk, deleted_at=None)
            serializer = ProductsSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def update(self, request, pk=None): 
        try:
            product = Products.objects.get(id=pk)
            serializer = ProductsSerializer(instance=product, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def destroy(self, request, pk=None):
        try:
            product = Products.objects.get(id=pk)
            product.delete()
            return Response({"response":"Product deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def product_search(self, request):
        try:
            queryset = Products.objects.filter(product_description__icontains=request.data["keyword"], deleted_at=None)
            serializer = ProductsSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


