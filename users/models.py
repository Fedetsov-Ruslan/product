from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

from courses.models import Course, Lesson


class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()


class Balance(models.Model):
    """Модель баланса пользователя."""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='balance')
    balance = models.PositiveIntegerField(default=1000)

    def save(self, *args, **kwargs):
        current_user = kwargs.pop('user', None)
        if self.balance < 0:
            raise ValidationError("Баланс не может быть отрицательным.")
        
        if current_user and not current_user.is_staff:
            raise PermissionError("Изменение баланса доступно только администраторам.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} - {self.balance} бонусов'
    # TODO сделал

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)


class Subscription(models.Model):
    """Модель подписки пользователя на курс."""
    
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    # TODO сделал

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)

