from django.urls import path

from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register("register",views.RegisterViewSet,basename="register")
router.register("login",views.LoginViewSet,basename="login")
router.register("users",views.UserViewSet,basename="users")

urlpatterns = [
    
]


urlpatterns+=router.urls