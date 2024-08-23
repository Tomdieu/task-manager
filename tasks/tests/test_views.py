import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from tasks.models import Task

@pytest.mark.django_db
def test_create_task(api_client):
    user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse('task-list')
    data = {
        'title': 'New Task',
        'description': 'Test description',
        'completed': False,
    }
    response = client.post(url, data, format='json')
    
    assert response.status_code == 201
    assert Task.objects.count() == 1
    assert Task.objects.get().title == 'New Task'

@pytest.mark.django_db
def test_task_list(api_client):
    user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
    client = APIClient()
    client.force_authenticate(user=user)
    
    Task.objects.create(title="Task 1", description="Description 1", user=user)
    Task.objects.create(title="Task 2", description="Description 2", user=user)
    
    url = reverse('task-list')
    response = client.get(url)
    
    assert response.status_code == 200
    assert len(response.data) == 2

@pytest.mark.django_db
def test_task_detail(api_client):
    user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
    client = APIClient()
    client.force_authenticate(user=user)
    
    task = Task.objects.create(title="Task 1", description="Description 1", user=user)
    
    url = reverse('task-detail', kwargs={'pk': task.pk})
    response = client.get(url)
    
    assert response.status_code == 200
    assert response.data['title'] == "Task 1"
