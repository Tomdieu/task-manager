from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Task
from django.contrib.auth import get_user_model

User = get_user_model()

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

    def get_queryset(self):
        return super(TaskDocument, self).get_queryset().select_related("user")

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, User):
            return related_instance.tasks.all()

    class Django:
        model = Task
        fields = [
            'title',
            'description',
            'completed',
            'created_at',
        ]

        related_models = [User]
