from rest_framework import serializers
from autheticate.models import User

class UserSerializer (serializers.ModelSerializer):
    class meta:
        model = User
        fields = ['id','email','firstname','lastname','phone','gender','created_at']