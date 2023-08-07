# serializer : 모델 ==> json | json ==> 모델 변환

from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ("id", "title", "complete", "important")
