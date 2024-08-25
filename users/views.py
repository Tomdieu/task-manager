from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .serializers import LoginSerializer, UserSerializer

User = get_user_model()


class LoginViewSet(GenericViewSet, CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {"message": "Invalid Credentials", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = Token.objects.get(user=user)

        login(request, user)
        return Response(
            {
                "token": token.key,
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "success": True,
            }
        )

class RegisterViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserViewSet(UpdateModelMixin,ListModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    pagination_class = PageNumberPagination
