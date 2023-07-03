from . import views
from django.urls import path

urlpatterns = [
    path("signup", views.SignupView.as_view()),
    path("login", views.LoginView.as_view()),
    path("logout", views.LogoutView.as_view()),
    path("friend_requests/sent", views.SentFriendRequestView.as_view()),
    path("friend_requests/received", views.ReceivedFriendRequestView.as_view()),
    path("friend_requests/received/<int:pk>", views.FriendRequestDetail.as_view()),
    path(
        "friend_requests/received/<int:pk>/accept", views.AcceptFriendRequest.as_view()
    ),
]
