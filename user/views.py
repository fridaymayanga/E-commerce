from django.shortcuts import render,get_object_or_404
from rest_framework import views, generics, status, permissions
from rest_framework.response import Response
from utils.pagination import CustomPagination
from autheticate.models import User
from user.serializers import UserSerializer

# Create your views here.

class HelloView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        return Response(data={"message":"Helloworld"}, status=200)