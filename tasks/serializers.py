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
            'created_at',
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)
        

class TaskDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Task
        fields = '__all__'