from .models import Task
from rest_framework import serializers
from users.serializers import UserSerializer


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = [
            "id",
            'title',
            'description',
            'completed',
            'user',
            'created_at',
        ]

class TaskDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Task
        fields = '__all__'