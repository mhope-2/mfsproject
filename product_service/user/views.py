from rest_framework import viewsets, status
from rest_framework.response import Response
import datetime
from rest_framework import generics, permissions
from rest_framework.decorators import action
from django.db import transaction


from rest_framework.authtoken.models import Token

from .models import User

from .serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt


from pathlib import Path
# Create your views here.

ROOT_DIR = Path('__file__').resolve().parent

import logging
logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ViewSet):

    # permission_classes = (permissions.AllowAny,)

    def list(self, request): 
        users = User.objects.filter(deleted_at=None)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @csrf_exempt
    @transaction.atomic
    def create(self, request): 
        try:

            serializer = UserSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                        "message": "User registration successful. Kindly check email for password.", 
                        "data": serializer.data
                        }, 
                        status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.debug(str(e))
            return Response({"response": str(e), "message": "User creation failed"}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None): 
        try:
            user = User.objects.get(id=pk, deleted_at=None)
            serializer = UserSerializer(user)
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    @transaction.atomic
    def update(self, request, pk=None): 
        try:
            user = User.objects.get(id=pk)
            serializer = UserSerializer(instance=user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"response": serializer.data, "message": "User update successful"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"response": str(e), "message": "User update failed"}, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    @transaction.atomic
    def destroy(self, request, pk=None):
        try:

            user = User.objects.get(id=pk)
            user.delete()

            return Response({"response":"User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(str(e))
            return Response({"response":str(e), "message": "User deletion failed"}, status=status.HTTP_400_BAD_REQUEST)


    # @csrf_exempt
    # @action(detail=False, methods=['post'])
    @transaction.atomic
    def fetch(self, request):
        try:
            user_id = Token.objects.get(key=request.data["auth_token"]).user_id
            user = User.objects.get(id=user_id, deleted_at=None)
            serializer = UserSerializer(user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"response": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    



# class RequestPasswordResetEmail(generics.GenericAPIView):
#     serializer_class = RequestPasswordResetEmailSerializer

#     def post(self, request, *args, **kwargs):
#         data = {'request':request, 'data': request.data}
#         serializer = self.serializer_class(data=request.data)

#         email = request.data['email']

#         if User.objects.filter(email=email).exists():
#             user = User.objects.get(email=email)
#             uidb64=urlsafe_base64_encode(smart_bytes(user.id))
#             token = PasswordResetTokenGenerator().make_token(user)
#             current_site = get_current_site(request=request).domain
#             relative_link = reverse('password-reset-confirm', kwargs={'uidb64':uidb64,'token':token})
#             absurl = 'http://'+str("https://amata.com")+str(relative_link)
#             email_body = 'Hi \nUse the link below to reset your password.\n ' + str(absurl)
#             data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Reset Password'}
            
#             # send email
#             send_email_task.delay(data=data)
#             # serializer.is_valid(raise_exception=True)
#             # serializer.save()
#             return Response({"response": "Password reset email sent"}, status=status.HTTP_200_OK)
#         else:
#             return Response({"response": "Error sending reset password to {}".format(str(data))})
        
 

# class PasswordTokenCheckAPI(generics.GenericAPIView):
#     def get(self, request, uidb64, token):
#         try:
#             id = smart_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(id=id)

#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 return Response({"response": "Token is not valid. Please request a new one."}, status=status.HTTP_401_UNAUTHORIZED)

#             return Response({"response": "Password reset link is valid", "success":True, "uidb64":uidb64, "token": token }, status=status.HTTP_200_OK)
#         except DjangoUnicodeDecodeError as e:
#             return Response({"response": "Token is not valid. Please request a new one."}, status=status.HTTP_401_UNAUTHORIZED)


# class SetNewPasswordAPIView(generics.GenericAPIView):
#     serializer_class = SetNewPasswordSerializer

#     def patch(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response({"response": "Password Reset was Successful", "success": True}, status=status.HTTP_200_OK)
