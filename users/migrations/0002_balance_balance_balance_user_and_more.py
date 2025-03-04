# Generated by Django 4.2.10 on 2024-08-16 16:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_price_lesson_course_id'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='balance',
            name='balance',
            field=models.PositiveIntegerField(default=1000),
        ),
        migrations.AddField(
            model_name='balance',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='balance', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='customer_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='group_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
            preserve_default=False,
        ),
    ]
