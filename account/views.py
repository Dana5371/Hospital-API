from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from account.models import User
from account.serializers import CreateNewPasswordSerializer, LoginSerializer, RegisterSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from account.utils import send_activation_code
# Create your views here.
# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Successfully signed up!', status=status.HTTP_201_CREATED)

class ActivateView(APIView):
    def get(self, request, activation_code):
        User = get_user_model()
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Your account successfully activated!', status=status.HTTP_200_OK)

class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('Successfully logged out', status=status.HTTP_200_OK)


class ResetPassword(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        try:
            user = User.objects.get(email=email)
            user.is_active = False
            user.create_activation_code()
            user.save()
            send_activation_code(user)
            return Response('Вам отправлено письмо', status=200)
        except User.DoesNotExist:
            return Response({'msg': 'User doesnt exist'}, status=status.HTTP_400_BAD_REQUEST)


class ResetComplete(APIView):
    def post(self, request):
        serializer = CreateNewPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Password reseted successfully', status=200)