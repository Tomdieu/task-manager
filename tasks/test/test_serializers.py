from tasks.serializers import TaskSerializer
from tasks.models import Task
from django.contrib.auth.models import User
import pytest

@pytest.mark.django_db
def test_valid_task_serializer():
    user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
    task_data = {
        'title': 'Test Task',
        'description': 'This is a test task',
        'completed': False,
        'user': user.id
    }
    serializer = TaskSerializer(data=task_data)
    assert serializer.is_valid()
    assert serializer.validated_data['title'] == 'Test Task'
    assert serializer.validated_data['description'] == 'This is a test task'
    assert serializer.validated_data['completed'] is False

@pytest.mark.django_db
def test_invalid_task_serializer():
    task_data = {
        'title': '',
        'description': 'This is a test task',
        'completed': False,
    }
    serializer = TaskSerializer(data=task_data)
    assert not serializer.is_valid()
    assert 'title' in serializer.errors
