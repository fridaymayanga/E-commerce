from rest_framework import serializers
from autheticate.models import User, GENDER_OPTIONS

class SignUpSerializer (serializers.ModelSerializer):
    gender =serializers.ChoiceField(choices=[x[0] for x in GENDER_OPTIONS])
    phone = serializers.CharField(max_length=14, min_length=14)
    password = serializers.CharField(min_length=8)
    class Meta:
        model = User
        fields = ['id','email','phone','address', 'password','firstname','lastname','gender']

        def validate_phone (self, obj):
            if not obj.startwith('+234'):
                raise serializres.ValidationError('Phone number must start with +234')
            return obj


class LoginSerializer(serializers.Serializer):
    email =serializers.EmailField()
    password = serializers.CharField()