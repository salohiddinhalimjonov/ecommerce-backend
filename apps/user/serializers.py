from rest_framework import serializers
from apps.user.models import UserModel


class SendPhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)


class VerifyPhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    code = serializers.CharField()
    session = serializers.CharField()

    def validate_code(self, value):
        if len(value) != 6:
            raise ValidationError('Code must be 6 digits!')
        else:
            return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            'id',
            'first_name',
            'last_name',
            'phone_number',
            'birth_date',
            'gender',
            'email'
        ]
        extra_kwargs = {
            'phone_number': {'read_only': True},
        }


class AdminLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class AdminCreateSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    admin_password = serializers.CharField(required=True)


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            'id',
            'first_name',
            'last_name',
            'phone_number',
            'birth_date',
            'gender',
            'email',
            'admin_password'
        ]
        extra_kwargs = {
            'phone_number': {'read_only': True},
        }