import email
import os
import string
import uuid
from hashlib import new
from random import random

from applications.account.authenticate import CustomAuthentication
from applications.account.models import Reset, User
from applications.account.serializers import ChangePasswordSerializer, UserSerializer
from applications.utils.email_sender import EmailSender
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, render
from django.template import Context
from django.urls import reverse
from django.utils.encoding import DjangoUnicodeDecodeError, force_str, smart_bytes, smart_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django_rest_passwordreset.signals import pre_password_reset, reset_password_token_created
from rest_framework import exceptions, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    response = Response({"message": "logout successful"})
    response.delete_cookie("refresh")
    return response


# Create your views here.
class UserAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JWTAuthentication,)

    def get(self, request):
        user = User.objects.filter(email=request.user).first()
        serializer = UserSerializer(user)
        return Response({"message": "success", "data": serializer.data})


class GetAllUsersAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class DeleteUserAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JWTAuthentication,)

    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        if user is not None:
            user.delete()
            return Response({'message': "success"})
        return Response({"message": "user not found"})


class RegisterAPIView(APIView):
    authentication_classes = ()
    permissssion_classes = ()

    def post(self, request):
        data = {}
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            data['response'] = "Registration Succesfull"
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            try:
                email_sender = EmailSender(from_email="info@pixelding.de",
                                           to=[request.data['email']], subject="Registrierung abschließen", context=serializer.data, template="register_email.html")

                email_sender.send_mail()
            except Exception as e:
                print("Email Error over here", e)
        else:
            data = serializer.errors
        return Response(data)


class ForgotAPIView(generics.UpdateAPIView):
    model = User
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(data={"error": "old_pass_error", "old_password": "Old Password is incorrect"}, status=status.HTTP_204_NO_CONTENT)

            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response({"errors": serializer.errors})


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    url = os.environ["CLIENT_URL_PUB"] + \
        'auth/reset/' + reset_password_token.key
    user = User.objects.filter(email=reset_password_token.user.email).first()
    user_serializer = UserSerializer(user)

    context = {"url": url, "email": email, }
    context['first_name'] = user_serializer.data['first_name']
    context['last_name'] = user_serializer.data['last_name']

    try:
        email_sender = EmailSender(from_email="info@pixelding.de",
                                   to=[reset_password_token.user.email], subject="Neues Passwort erstellen ", context=context, template="new_password_email.html")
    except Exception as e:
        print(e)
    email_sender.send_mail()


@receiver(pre_password_reset)
def password_reset_middleware(sender, instance, reset_password_token, *args, **kwargs):
    print("afdasdfasddfsadsfadsfasdfds ", sender, instance, reset_password_token, *args, **kwargs)

class ResetAPIView(APIView):
    def post(self, request):
        print("I ran")

        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl+"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            send_mail(data)
            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class AddProfileImageAPIView(APIView):
    def put(self, request, pk):
        data = request.FILES
        user = User.objects.filter(pk=pk).first()
        serializer = UserSerializer(instance=user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
