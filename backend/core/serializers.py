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
