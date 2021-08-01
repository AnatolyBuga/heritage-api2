import os
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.utils.six import text_type
# from .constants import ACCOUNT_NOT_FOUND
from .models import User
from utils.aws import generate_aws_url
from django.core.validators import RegexValidator



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        self.user = authenticate(**{
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
        })

        # if self.user is None:
        #     raise serializers.ValidationError(ACCOUNT_NOT_FOUND)

        refresh = self.get_token(self.user)

        return {
            'email': self.user.email,
            'refresh': text_type(refresh),
            'access': text_type(refresh.access_token),
        }


class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    def get_avatar_url(self, obj):
        bucket_name = os.getenv('AWS_AVATAR_IMAGE_BUCKET_NAME')
        content_type = 'image/png'
        return generate_aws_url(key=obj.avatar_url, bucket=bucket_name, content_type=content_type)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'user_role', 'first_name', 'last_name', 'bio', 'avatar_url')


class CreateUserSerializer(serializers.Serializer):
    username_validator = RegexValidator("^[a-zA-Z0-9_.-]{4,25}$",
                                        "username can only contain alphanumeric characters, ., _,-")
    password_validator = RegexValidator("^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]).{8,32}$",
                                        "password must contain at least an Uppercase, lowercase and a number")

    email = serializers.EmailField()
    username = serializers.CharField(validators=[username_validator])
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(validators=[password_validator])
    bio = serializers.CharField()
