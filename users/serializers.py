from rest_framework.serializers import Serializer, ModelSerializer

from django.contrib.auth.models import User
# from users.models import User


# class UserSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'password', 'create_at', 'update_at']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
