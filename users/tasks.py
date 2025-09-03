from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import User


@shared_task
def check_inactive_users():
    """
    Проверяет пользователей, которые не заходили более месяца и блокирует их
    """
    month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=month_ago, is_active=True)

    count = inactive_users.count()
    inactive_users.update(is_active=False)

    return f"Заблокировано {count} неактивных пользователей"
