from django.db import models
from django.conf import settings




class Course(models.Model):
    """Модель продукта - курса."""

    author = models.CharField(
        max_length=250,
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    start_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата и время начала курса'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2, 
        default=0.00,
        verbose_name='Цена',
    )

    # TODO сделал

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    link = models.URLField(
        max_length=250,
        verbose_name='Ссылка',
    )

    # TODO сделал

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Group(models.Model):
    """Модель группы."""

    # TODO 
    from users.models import CustomUser
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='groups')
    max_students = models.IntegerField(default=30)
    students = models.ManyToManyField(CustomUser, related_name='course_groups')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)

    def __str__(self):
        return self.name if self.name else f"Group {self.id} for {self.course.title}"
    
    def add_student(self, student):
        """Добавить студента в группу, если есть свободные места."""
        if self.students.count() < self.max_students:
            self.students.add(student)
        else:
            raise ValueError("Группа заполнена.")    
