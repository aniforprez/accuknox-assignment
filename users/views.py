from rest_framework import mixins, generics, throttling
from rest_framework.views import APIView, Response, status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serialisers import (
    SignupSerialiser,
    LoginSerialiser,
    FriendRequestSerialiser,
    UserSerialiser,
)
from .models import User, FriendRequest
from django.db.models import Q
from itertools import chain


class SignupView(APIView):
    def post(self, request, format=None):
        serializer = SignupSerialiser(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
            )
            return Response({"success": True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = LoginSerialiser

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class SearchUsersView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerialiser

    def get_queryset(self):
        queryset = User.objects.all()
        email_query = self.request.query_params.get("email")
        name_query = self.request.query_params.get("name")
        results = []

        if email_query:
            results = queryset.filter(email=email_query)
        elif name_query:
            results = queryset.filter(
                Q(first_name__contains=name_query) | Q(last_name__contains=name_query)
            )

        return results


class FriendsView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerialiser

    def get_queryset(self):
        current_user = self.request.user
        results = set()
        for fr in FriendRequest.objects.select_related("from_user").filter(
            to_user=current_user
        ):
            results.add(fr.to_user)
        for fr in FriendRequest.objects.select_related("to_user").filter(
            from_user=current_user
        ):
            results.add(fr.to_user)

        return results


class SentFriendRequestListView(mixins.ListModelMixin, generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerialiser

    def get_queryset(self):
        return FriendRequest.objects.filter(from_user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SendFriendRequestThrottle(throttling.UserRateThrottle):
    rate = "3/m"


class SendFriendRequestView(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerialiser
    throttle_classes = [SendFriendRequestThrottle]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ReceivedFriendRequestListView(mixins.ListModelMixin, generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerialiser

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PendingFriendRequestView(mixins.ListModelMixin, generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerialiser

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, accepted=None)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class FriendRequestDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        current_user = self.request.user
        try:
            return FriendRequest.objects.filter(
                Q(to_user=current_user) | Q(from_user=current_user)
            ).get(pk=pk)
        except FriendRequest.DoesNotExist:
            raise

    def get(self, request, pk, format=None):
        try:
            fr = self.get_object(pk)
        except FriendRequest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FriendRequestSerialiser(fr)
        return Response(serializer.data)


class AcceptFriendRequest(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user)

    def post(self, request, *args, **kwargs):
        try:
            fr = self.get_object()
        except FriendRequest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        fr.accepted = True
        fr.save()
        serializer = FriendRequestSerialiser(fr)
        return Response(serializer.data)


class RejectFriendRequest(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user)

    def post(self, request, *args, **kwargs):
        try:
            fr = self.get_object()
        except FriendRequest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        fr.accepted = False
        fr.save()
        serializer = FriendRequestSerialiser(fr)
        return Response(serializer.data)
