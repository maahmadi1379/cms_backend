from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class SoftDeleteBaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created Date Time')
    updated = models.DateTimeField(auto_now=True, verbose_name='Updated Date Time')
    deleted = models.DateTimeField(null=True, blank=True, verbose_name='Deleted Date Time')
    is_deleted = models.BooleanField(default=False, verbose_name='Is Deleted')

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted = timezone.now()
        self.save()


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Session(models.Model):
    label = models.CharField(max_length=255)
    # session period
    start = models.DateTimeField()
    end = models.DateTimeField()
    # session select unit period
    start_select_unit = models.DateTimeField()
    end_select_unit = models.DateTimeField()
    # session remove add period
    start_remove_add = models.DateTimeField()
    end_remove_add = models.DateTimeField()


class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    session = models.ForeignKey(Session, on_delete=models.PROTECT)
    is_active = models.BooleanField()


class Course(models.Model):
    label = models.CharField(max_length=255)
    unit = models.PositiveSmallIntegerField()


class SessionCourse(models.Model):
    session = models.ForeignKey(Session, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)


class UserSessionCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    session_course = models.ForeignKey(SessionCourse, on_delete=models.PROTECT)
    final_score = models.PositiveSmallIntegerField(null=True, blank=True)
    midterm_score = models.PositiveSmallIntegerField(null=True, blank=True)


class SessionCourseClass(models.Model):
    WEEK_DAYS = [
        (1, 'Saturday'),
        (2, 'Sunday'),
        (3, 'Monday'),
        (4, 'Tuesday'),
        (5, 'Wednesday'),
        (6, 'Thursday'),
        (7, 'Friday'),
    ]
    session_course = models.ForeignKey(SessionCourse, on_delete=models.PROTECT)
    day_of_week = models.CharField(choices=WEEK_DAYS)
    label = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
