from rest_framework import serializers
from .models import User, FriendRequest
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
        fields = ["id", "email", "first_name", "last_name"]


class FriendRequestSerialiser(serializers.ModelSerializer):
    from_user = UserSerialiser(read_only=True)
    to_user = UserSerialiser(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ["id", "from_user", "to_user", "accepted"]

    def validate(self, attrs):
        request = self.context.get("request")
        user_id = request.user.id

        to_user_id = request.data.get("to_user")
        if to_user_id == user_id:
            raise serializers.ValidationError("Cannot send friend requests to yourself")

        try:
            to_user = User.objects.get(pk=to_user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")

        attrs["from_user"] = request.user
        attrs["to_user"] = to_user
        return super().validate(attrs)

    def create(self, validated_data):
        return super().create(validated_data)
