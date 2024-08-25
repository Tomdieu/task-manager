import pytest
from django.contrib.auth.models import User
from tasks.models import Task

@pytest.mark.django_db
def test_task_creation():
    user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
    task = Task.objects.create(
        title="Test Task",
        description="This is a test task",
        user=user
    )
    assert task.title == "Test Task"
    assert task.description == "This is a test task"
    assert task.user == user
    assert task.completed is False
