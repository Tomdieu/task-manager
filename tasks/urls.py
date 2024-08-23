from rest_framework.routers import DefaultRouter

from .views import TaskViewSet

router = DefaultRouter()

router.register("tasks",viewset=TaskViewSet,basename="tasks")

urlpatterns = [
    
]

urlpatterns += router.urls
