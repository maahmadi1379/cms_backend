from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import (
    CourseViewSet,
    SessionViewSet,
    AdminChangePasswordUserViewSet,
    StudentChangePasswordUserViewSet,
    CreateUpdateListRetrieveDestroyUserViewSet,
)

router = DefaultRouter()
router.register(r'course', CourseViewSet)
router.register(r'session', SessionViewSet)
router.register(r'user', CreateUpdateListRetrieveDestroyUserViewSet, basename='CRUD-user')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin-change-password/', AdminChangePasswordUserViewSet.as_view(), name='change_password_admin'),
    path('student-change-password/', StudentChangePasswordUserViewSet.as_view(), name='change_password_student'),

    # TODO: completed (+), uncompleted (-)
    # Student:
    #   + session/ (GET)
    #   - session/<id>/exists-course/ (GET)
    #   - session/<id>/select-unit/ (PUT)
    #   - session/<id>/remove-add/ (PUT)
    #   - session/<id>/select-course/ (GET)
    #   - session/<id>/select-course/<id>/classes/ (GET)
    #   - session/<id>/select-course/<id>/scores/ (GET)

    # Staff or Teacher:
    #   + session/ (CRUD)
    #   + course/ (CRUD)
    #   - session/<id>/exists-course/ (GET, PUT)
    #   - session/<id>/exists-course/<id>/classes/ (GET, PUT)
    #   + user/ (GET)
    #   - session/<id>/user/<id>/course/<id>/scores/ (GET, PUT)

    # Admin:
    #   - ...
    #   + user/ (CRUD)
]
