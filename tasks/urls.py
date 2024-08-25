from django.urls import path, re_path
from rest_framework.routers import DefaultRouter

from .views import TaskViewSet, SearchTaskView

router = DefaultRouter()

router.register("tasks", viewset=TaskViewSet, basename="tasks")

urlpatterns = [
    re_path(r'tasks/search/(?P<query>\w+)/?', SearchTaskView.as_view(), name="search-tasks") 
]

urlpatterns += router.urls