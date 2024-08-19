from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, ExpressionWrapper, FloatField
from api.v1.permissions import make_payment
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer)
from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course
from users.models import Subscription
import logging

class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.groups.all()

class AvailableCoursesViewSet(viewsets.ModelViewSet):
    """Доступные к покупке курсы."""

    permission_classes = (ReadOnlyOrIsAdmin,)
    def get_queryset(self):
        """Возникла проблема с аутентификацией. Сделал через токены."""
        client = APIClient()
        token = 'bf172b1bcc022ddac065d756740253622ba0552c'
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        user = Token.objects.get(key=token).user
        
        queryset = Course.objects.all().exclude(
                subscription__customer_id=user
            ).annotate(
                lessons_count=Count('lesson')
            ).order_by('id')
        permission_classes = (ReadOnlyOrIsAdmin,)
        return queryset

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы """

    queryset = Course.objects.all().annotate(
        lessons_count=Count('lesson', distinct=True),
        students_count=Count('subscription__customer_id', distinct=True),
        groups_filled_percent=ExpressionWrapper(
            (Count('subscription__customer_id', distinct=True) / 30.0) * 100,
            output_field=FloatField()
        )
    ).order_by('id')
    permission_classes = (ReadOnlyOrIsAdmin,)
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def pay(self, request, pk):
        """Покупка доступа к курсу (подписка на курс)."""
        
        course = self.get_object()
        res = make_payment(request, course)
        # TODO сделал
        
        return Response(
            data=res["detail"],
            status=res['status']
        )
