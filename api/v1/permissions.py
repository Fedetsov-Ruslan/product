from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import Subscription
from courses.models import Course, Group
from django.db import transaction
from django.db.models import F, Count
from django.shortcuts import get_object_or_404
from rest_framework import status


def make_payment(request, course_id):
    # TODO
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    if user.balance < course.price:
        return {"detail": "Недостаточно бонусов для покупки курса.",
                'status':status.HTTP_400_BAD_REQUEST}
    """Добавляем студента в Subscription, затем добавляем студента в группу"""      
    with transaction.atomic():
        user.balance -= course.price
        user.save()
        Subscription.objects.create(customer_id=user.id, group_id=course.id)
        group = Group.objects.filter(
                course=course, 
                students__lt=30
            ).annotate(
                students_count=Count('students')  
            ).order_by('students_count').first()

        if not group:
            group = Group.objects.create(course=course, max_students=30)
        group.add_student(user)


    return {"detail": "Курс успешно куплен и вы добавлены в группу.",
            'status': status.HTTP_201_CREATED}
    


class IsStudentOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        # TODO
        if request.user.is_staff:
            return True
        return request.user.is_authenticated and hasattr(request.user, 'is_student') and request.user.is_student


    def has_object_permission(self, request, view, obj):
        # TODO
        if request.user.is_staff:
            return True 
        return Subscription.objects.filter(customer_id=request.user, group_id=obj).exists()


class ReadOnlyOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS
