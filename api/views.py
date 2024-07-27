from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema

from api.models import (
    Course,
    Session,
)
from api.serializers import (
    CourseSerializer,
    SessionSerializer,
    CreateUserSerializer,
    UpdateUserSerializer,
    ListRetrieveDestroyUserSerializer,
    StudentChangePasswordUserSerializer,
    AdminChangePasswordUserSerializer,
)
from utils.permissions import IsAdmin, IsStudent
from utils.paginations import CustomPageNumberPagination


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('-id')
    serializer_class = CourseSerializer
    pagination_class = CustomPageNumberPagination


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all().order_by('-id')
    serializer_class = SessionSerializer
    pagination_class = CustomPageNumberPagination


class AdminChangePasswordUserViewSet(GenericAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsAdmin)

    @swagger_auto_schema(
        request_body=AdminChangePasswordUserSerializer,
    )
    def put(self, request, *args, **kwargs):
        serializer = AdminChangePasswordUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentChangePasswordUserViewSet(GenericAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsStudent)

    @swagger_auto_schema(
        request_body=StudentChangePasswordUserSerializer,
    )
    def put(self, request, *args, **kwargs):
        serializer = StudentChangePasswordUserSerializer(
            data=request.data,
            context={
                'request': request
            }
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateUpdateListRetrieveDestroyUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = ListRetrieveDestroyUserSerializer
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action in ['create']:
            return CreateUserSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateUserSerializer
        elif self.action in ['create', 'list', 'retrieve', 'destroy']:
            return ListRetrieveDestroyUserSerializer
        else:
            raise ValueError("Invalid action")
