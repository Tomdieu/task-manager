import pytest
from rest_framework.test import APIClient
from django.conf import settings
from django.core.management import call_command
from django.db import connection
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'task_manager_test',  # Use the test database name from the Docker Compose file
        'USER': 'task_manager',        # Match the POSTGRES_USER from Docker Compose
        'PASSWORD': 'task_manager',    # Match the POSTGRES_PASSWORD from Docker Compose
        'HOST': 'localhost',           # The service is running on localhost
        'PORT': '5433',                # Use the port from the test_db service in Docker Compose
        'ATOMIC_REQUESTS': True,       # Ensure atomic requests are enabled
    }

@pytest.fixture(scope='session', autouse=True)
def apply_migrations(django_db_setup, django_db_blocker):
    """
    Apply database migrations before running tests.
    """
    with django_db_blocker.unblock():
        call_command('migrate', verbosity=0)

@pytest.fixture
def api_client():
    return APIClient()
