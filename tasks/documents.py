from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Task

@registry.register_document
class TaskDocument(Document):
    # Define a field for the username from the related User model
    user = fields.ObjectField(properties={
        'username': fields.TextField(),
    })

    class Index:
        name = "tasks"

    settings = {
        "number_of_shards": 1,
        "number_of_replicas": 0,
    }

    class Django:
        model = Task
        fields = [
            'title',
            'description',
            'completed',
            'created_at',
        ]
