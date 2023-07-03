from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import User
from django.contrib.auth import authenticate


class SignupSerialiser(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)


class LoginSerialiser(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(min_length=8, write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"),
                username=email,
                password=password,
            )

            if not user:
                raise serializers.ValidationError(
                    "Unable to log in with provided credentials.", code="authorization"
                )
        else:
            raise serializers.ValidationError(
                'Must include "email" and "password".', code="authorization"
            )

        attrs["user"] = user
        return attrs


class UserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]
