from . import views
from django.urls import path

urlpatterns = [
    path("signup", views.SignupView.as_view()),
    path("login", views.LoginView.as_view()),
    path("logout", views.LogoutView.as_view()),
    path("users", views.SearchUsersView.as_view()),
    path("friends", views.FriendsView.as_view()),
    path("friend_requests", views.SendFriendRequestView.as_view()),
    path("friend_requests/sent", views.SentFriendRequestListView.as_view()),
    path("friend_requests/received", views.ReceivedFriendRequestListView.as_view()),
    path("friend_requests/received/pending", views.PendingFriendRequestView.as_view()),
    path("friend_requests/received/<int:pk>", views.FriendRequestDetail.as_view()),
    path(
        "friend_requests/received/<int:pk>/accept", views.AcceptFriendRequest.as_view()
    ),
    path(
        "friend_requests/received/<int:pk>/reject", views.RejectFriendRequest.as_view()
    ),
]
