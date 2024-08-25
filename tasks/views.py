from django.http import JsonResponse
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from elasticsearch_dsl.query import Q
from rest_framework import status
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .documents import TaskDocument
from .models import Task
from .serializers import TaskSerializer

# Create your views here.

class TaskViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    @swagger_auto_schema(
        operation_description="Search articles",
        manual_parameters=[
            openapi.Parameter(
                name="page",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=False,
                description="Page number for pagination",
            ),
            openapi.Parameter(
                name="query",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description="Search tesk by name ,description or owner",
            )
        ],
    )
    @action(methods=['GET'],detail=False)
    def search(self,request,query):

        try:
            q = Q(
                "query_string",
                query="*" + query + "*",
                fields=[
                    "title",
                    "description",
                    "user.username"
                    
                ],
                fuzziness="auto",
            )

            search = self.search_document.search()
            search = search.query(q)
            response = search.execute()

            paginator = self.pagination_class()
            paginated_response = paginator.paginate_queryset(
                response, request, view=self
            )

            if paginated_response is not None:
                serializer = self.search_serializer(paginated_response, many=True)
                return paginator.get_paginated_response(serializer.data)

            serializer = self.search_serializer(response, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    
