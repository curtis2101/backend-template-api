from user_info.models import UserInfo
from rest_framework import serializers
from users.serializers import UserSerializer


class GetUserInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserInfo
        fields = '__all__'
