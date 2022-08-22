import logging
from .models import Customer
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import CustomerSerializer
from django.db import transaction

logger = logging.getLogger(__name__)


# Create your views here.
class CustomerViewSet(viewsets.GenericViewSet):

    # permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):
        customers = Customer.objects.filter(deleted_at=None)
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        try:
            request_data = request.data
            request_data["customer_code"] = self.generate_customer_code()

            serializer = CustomerSerializer(data=request_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                {
                    "response": serializer.data,
                    "message": "Successfully created customer",
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"response": str(e), "message": "Error creating customer"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def retrieve(self, request, pk=None):
        try:
            customer = Customer.objects.get(id=pk, deleted_at=None)
            serializer = CustomerSerializer(customer)
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e))
            return Response({"response": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            customer = Customer.objects.get(id=pk, deleted_at=None)
            serializer = CustomerSerializer(instance=customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    "response": serializer.data,
                    "message": "Successfully updated customer details",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"response": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            customer = Customer.objects.get(id=pk)
            customer.delete()
            return Response(
                {"response": "customer deleted successfully"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(str(e))
            return Response(
                {"response": str(e), "message": "Error deleting customer"},
                status=status.HTTP_404_NOT_FOUND,
            )

    # function to make items sequential
    def generate_customer_code(self):
        try:
            with transaction.atomic():
                # check for latest customer code
                logger.debug(
                    "last Customer Code: {}".format(
                        str(Customer.objects.latest("created_at")).split("|")[0]
                    )
                )
                latest_customer_code = int(
                    str(Customer.objects.latest("created_at"))
                    .split("|")[0]
                    .strip("CUS")
                )
                customer_code = "CUS" + str(latest_customer_code + 1)
                logger.info("GENERATED CUS CODE: {}".format(customer_code))
        except Exception as e:
            latest_customer_code = 0
            customer_code = str("CUS" + str(latest_customer_code + 1))

        return customer_code
