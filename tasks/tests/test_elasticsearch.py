import pytest
from django.contrib.auth.models import User
from tasks.models import Task
from tasks.documents import TaskDocument
from elasticsearch.exceptions import NotFoundError

@pytest.mark.django_db
def test_indexing_task_to_elasticsearch():
    # Create a user and task
    user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
    task = Task.objects.create(
        title="Elasticsearch Task",
        description="This task should be indexed in Elasticsearch.",
        user=user
    )
    
    # Fetch the task from Elasticsearch
    es_task = TaskDocument.get(id=task.id)
    
    # Check that the task is indexed correctly
    assert es_task.title == "Elasticsearch Task"
    assert es_task.description == "This task should be indexed in Elasticsearch."
    assert es_task.user.username == "testuser"

@pytest.mark.django_db
def test_search_task_in_elasticsearch():
    # Create a user and task
    user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
    Task.objects.create(
        title="Searchable Task",
        description="This task should be searchable in Elasticsearch.",
        user=user
    )

    # Perform a search query
    search_query = TaskDocument.search().query("match", title="Searchable Task")
    results = search_query.execute()
    
    # Ensure the task is found in Elasticsearch
    assert len(results) > 0
    assert results[0].title == "Searchable Task"
    assert results[0].description == "This task should be searchable in Elasticsearch."

@pytest.mark.django_db
def test_task_not_in_elasticsearch():
    # Try to fetch a non-existent task from Elasticsearch
    with pytest.raises(NotFoundError):
        TaskDocument.get(id=999)
