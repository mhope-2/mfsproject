import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from rest_framework.authtoken.models import Token
from .models import User
from .serializers import UserSerializer

from pathlib import Path

ROOT_DIR = Path('__file__').resolve().parent
try:
    logging.basicConfig(filename=f'{ROOT_DIR}/logs/product_service.log',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        level=logging.DEBUG)
except FileNotFoundError:
    pass

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ViewSet):

    # permission_classes = (permissions.AllowAny,)

    def list(self, request):
        users = User.objects.filter(deleted_at=None)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    @transaction.atomic
    def create(self, request):
        try:
            serializer = UserSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    "message": "User registration successful. Kindly check email for password.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            logger.debug(str(e))
            return Response(
                {"response": str(e), "message": "User creation failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(id=pk, deleted_at=None)
            serializer = UserSerializer(user)
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e))
            return Response({"response": str(e)}, status=status.HTTP_404_NOT_FOUND)

    
    @transaction.atomic
    def update(self, request, pk=None):
        try:
            user = User.objects.get(id=pk)
            serializer = UserSerializer(instance=user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"response": serializer.data, "message": "User update successful"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"response": str(e), "message": "User update failed"},
                status=status.HTTP_404_NOT_FOUND,
            )

    
    @transaction.atomic
    def destroy(self, request, pk=None):
        try:

            user = User.objects.get(id=pk)
            user.delete()

            return Response(
                {"response": "User deleted successfully"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(str(e))
            return Response(
                {"response": str(e), "message": "User deletion failed"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @transaction.atomic
    def fetch(self, request):
        try:
            user_id = Token.objects.get(key=request.data["auth_token"]).user_id
            user = User.objects.get(id=user_id, deleted_at=None)
            serializer = UserSerializer(user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"response": str(e)}, status=status.HTTP_400_BAD_REQUEST)
