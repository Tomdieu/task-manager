from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from elasticsearch_dsl import Search
from .models import Task
from .documents import TaskDocument

class TaskElasticsearchTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.task_data = {'title': 'Test Task', 'description': 'This is a test task.'}
        self.task = Task.objects.create(**self.task_data)
        self.task_document = TaskDocument()

    def test_task_indexing_in_elasticsearch(self):
        # Index the task in Elasticsearch
        self.task_document.update(self.task)

        # Refresh the index to make sure the document is searchable
        self.task_document._index.refresh()

        # Search for the task in Elasticsearch
        search = Search(using=self.task_document._get_connection(), index='tasks')
        search_response = search.query('match', title='Test Task').execute()

        # Assert the task is found in Elasticsearch
        self.assertEqual(len(search_response.hits), 1)
        self.assertEqual(search_response.hits[0].title, self.task_data['title'])

    def test_task_creation_and_indexing(self):
        url = reverse('task-list')
        response = self.client.post(url, self.task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Index the newly created task
        new_task = Task.objects.get(title=self.task_data['title'])
        self.task_document.update(new_task)

        # Refresh the index and search
        self.task_document._index.refresh()
        search = Search(using=self.task_document._get_connection(), index='tasks')
        search_response = search.query('match', title='Test Task').execute()

        # Assert the task is indexed
        self.assertEqual(len(search_response.hits), 1)
        self.assertEqual(search_response.hits[0].title, self.task_data['title'])
