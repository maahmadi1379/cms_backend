from django.contrib.auth.models import User, AnonymousUser
from rest_framework import serializers

from api.models import (
    Course,
    Session,
)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'is_active',
            'is_superuser',
        )


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'is_active',
            'is_superuser',
            'date_joined',
            'last_login',
        )


class ListRetrieveDestroyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'is_active',
            'is_superuser',
            'date_joined',
            'last_login',
        )


class AdminChangePasswordUserSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    user_id = serializers.IntegerField(required=True)

    def validate(self, attrs):
        user_obj = AnonymousUser()
        try:
            user_obj = User.objects.get(pk=attrs['user_id'])
        except User.DoesNotExist:
            raise serializers.ValidationError("The user does not exist.")

        if not user_obj.check_password(attrs['old_password']):
            raise serializers.ValidationError("Old password is incorrect.")

        if not attrs['new_password'].isalnum():
            raise serializers.ValidationError("The password must contain at least one alphanumeric character.")

        user_obj.set_password(self.validated_data['new_password'])
        user_obj.save()
        return attrs


class StudentChangePasswordUserSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        user_obj = self.context['request'].user

        if not user_obj.check_password(attrs['old_password']):
            raise serializers.ValidationError("Old password is incorrect.")

        if not attrs['new_password'].isalnum():
            raise serializers.ValidationError("The password must contain at least one alphanumeric character.")

        user_obj.set_password(self.validated_data['new_password'])
        user_obj.save()
        return attrs
