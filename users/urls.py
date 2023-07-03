from . import views
from django.urls import path

urlpatterns = [
    path("signup", views.SignupView.as_view()),
    path("login", views.LoginView.as_view()),
    path("logout", views.LogoutView.as_view()),
]
