from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from autheticate.serializers import SignUpSerializer, LoginSerializer
from autheticate.models import User
from django.contrib import auth

class SignUpView (generics.GenericAPIView):
    serializer_class = SignUpSerializer
    def post (self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email =serializer.validated_data.get ('email')
        password = serializer.validated_data.get ('password')
        email_exists = User.objects.filter (email=email).first()
        if email_exists:
            return response(data={'message': 'Account with email already exists'}, status=400)
        user = serializer.save()
        user.set_password(password)
        user.save()
        return Response(data={"message": "Account created succesfully"}, status=201)
# Create your views here.

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
        user = auth.authenticate(email=email, password=password)
        if not user:
            return Response(data={"message":"Invalid credentials"}, status=400)
        return Response(data=user.get_tokens(), status=200)
