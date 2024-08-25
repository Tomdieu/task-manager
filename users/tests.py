import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_user_registration(api_client):
    url = reverse('register-list')
    data = {
        'username': 'ivantom',
        'password': 'newpassword123',
        'email': 'ivantom@example.com',
        'first_name': 'New',
        'last_name': 'User'
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == 201
    assert User.objects.count() == 1
    assert User.objects.get().username == 'ivantom'


@pytest.mark.django_db
def test_user_login(api_client):
    user = User.objects.create_user(username='testuser_1', password='testpassword123')

    url = reverse('login-list')
    data = {
        'username': 'testuser_1',
        'password': 'testpassword123'
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == 200
    assert 'token' in response.data
    assert response.data['user']['username'] == 'testuser_1'


@pytest.mark.django_db
def test_user_list(api_client):
    user = User.objects.create_user(username='testuser_1', password='testpassword123')
    api_client.force_authenticate(user=user)

    url = reverse('users-list')
    response = api_client.get(url, format='json')

    assert response.status_code == 200
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['username'] == 'testuser_1'


@pytest.mark.django_db
def test_user_retrieve(api_client):
    user = User.objects.create_user(username='testuser_1', password='testpassword123')
    api_client.force_authenticate(user=user)

    url = reverse('users-detail', kwargs={'pk': user.pk})
    response = api_client.get(url, format='json')

    assert response.status_code == 200
    assert response.data['username'] == 'testuser_1'


@pytest.mark.django_db
def test_user_update(api_client):
    user = User.objects.create_user(username='testuser_1', password='testpassword123')
    api_client.force_authenticate(user=user)

    url = reverse('users-detail', kwargs={'pk': user.pk})
    data = {
        'first_name': 'Updated',
        'last_name': 'Name',
    }
    response = api_client.patch(url, data, format='json')

    assert response.status_code == 200
    assert response.data['first_name'] == 'Updated'
    assert response.data['last_name'] == 'Name'


@pytest.mark.django_db
def test_user_delete(api_client):
    user = User.objects.create_user(username='testuser_1', password='testpassword123')
    api_client.force_authenticate(user=user)

    url = reverse('users-detail', kwargs={'pk': user.pk})
    response = api_client.delete(url, format='json')

    assert response.status_code == 204
    assert User.objects.count() == 0
