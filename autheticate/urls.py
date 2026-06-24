from django.urls import path
from autheticate.views import SignUpView, LoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns =[
    path("signup/", SignUpView.as_view()),
    path("login/", LoginView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
]