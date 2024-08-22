from random import randint
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import authentication, permissions
from .serializers import SendPhoneNumberSerializer, VerifyPhoneNumberSerializer, UserSerializer, AdminLoginSerializer, AdminCreateSerializer,AdminSerializer
from .models import UserModel
from django.contrib.auth.hashers import make_password
from .services import send_verification_code, CacheTypes, generate_cache_key


class SendPhoneNumberView(APIView):
    permission_classes = [AllowAny,]

    def post(self, request, *args, **kwargs):
        serializer = SendPhoneNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get('phone_number')
        session = str(randint(100000, 999999))
        cache_key = send_verification_code(phone, CacheTypes.registration_sms_verification, session)
        cache_value = cache.get(cache_key)
        return Response({"code": cache_value, "session": session})


class VerifyPhoneNumberView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = VerifyPhoneNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get('phone_number')
        code = serializer.validated_data.get('code')
        session = serializer.validated_data.get('session')
        cache_key = generate_cache_key(CacheTypes.registration_sms_verification, phone, session)
        if not self.is_code_valid(cache_key, code):
            return Response(
                {"detail": "Wrong code!"}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            user = UserModel.objects.filter(phone_number=phone).first()
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=status.HTTP_201_CREATED)
            else:
                UserModel.objects.create(phone_number=phone)
                token = Token.objects.create(user=user)
                return Response({"token": token.key}, status=status.HTTP_201_CREATED)

    @staticmethod
    def is_code_valid(cache_key, code):
        valid_code = cache.get(cache_key)
        if valid_code != code:
            return False
        return True


class UserMeApiView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()
        return Response({'status': 'Logout successful!'}, status=status.HTTP_200_OK)


class AdminLoginView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get('phone_number')
        password = serializer.validated_data.get('password')
        user = UserModel.objects.filter(phone_number=phone_number, is_staff=True).first()
        if not user:
            return Response({'status': 'You are not a staff user!'}, status=status.HTTP_400_BAD_REQUEST)
        elif not check_password(password, user.admin_password):
            return Response({'status': 'Incorrect password!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)


class AdminView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'status': 'Only superuser is allowed to create staff or super user!'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = AdminCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get('phone_number')
        admin_password = serializer.validated_data.get('admin_password')
        try:
            user = UserModel.objects.get(phone_number=phone_number)
            user.is_staff = True
        except ObjectDoesNotExist:
            user = UserModel.objects.create(phone_number=phone_number, admin_password=admin_password, is_staff=True)
        else:
            user.admin_password = admin_password
            user.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        serializer = AdminSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        serializer = AdminSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteAdminView(APIView):
    permisssion_classes = [IsAuthenticated,]

    def delete(self, request, pk, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'status': 'Only superuser is allowed to delete staff user!'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = UserModel.objects.filter(id=pk, is_staff=True).first()
        if user:
            user.delete()
            return Response({'status': 'User has benn successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'status': 'There is no user with this id'}, status=status.HTTP_400_BAD_REQUEST)





