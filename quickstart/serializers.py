from django.contrib.auth.models import User, Group
from rest_framework import serializers

# 모델들을 시리얼 라이저로 엮는거 같음
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
