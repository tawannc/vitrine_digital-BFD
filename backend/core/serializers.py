from rest_framework import serializers
from .models import User

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'nome', 'password', 'aceita_termos']

    def validate_aceita_termos(self, value):
        if not value:
            raise serializers.ValidationError(
                "É necessário aceitar os termos para se cadastrar."
            )
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        return user

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            email=data['email'],
            password=data['password']
        )

        if not user:
            raise serializers.ValidationError("Credenciais inválidas.")

        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "email": user.email,
                "nome": user.nome,
                "tipo_usuario": user.tipo_usuario
            }
        }

import uuid
from django.utils import timezone
from datetime import timedelta


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Usuário não encontrado.")
        return value

    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        token = uuid.uuid4().hex

        user.reset_password_token = token
        user.reset_password_expires = timezone.now() + timedelta(hours=1)
        user.save()

        return token

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)

    def validate(self, data):
        user = User.objects.filter(
            reset_password_token=data['token'],
            reset_password_expires__gte=timezone.now()
        ).first()

        if not user:
            raise serializers.ValidationError("Token inválido ou expirado.")

        data['user'] = user
        return data

    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.reset_password_token = None
        user.reset_password_expires = None
        user.save()
