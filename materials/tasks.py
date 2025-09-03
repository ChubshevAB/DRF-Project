from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from materials.models import Subscription, Course


@shared_task
def send_course_update_notification(course_id):
    """
    Асинхронная отправка email подписанным пользователям об обновлении курса.
    """
    try:
        course = Course.objects.get(id=course_id)
        subscriptions = Subscription.objects.filter(course=course)
        recipients = [sub.user.email for sub in subscriptions if sub.user.email]

        if recipients:
            subject = f'Обновление материалов курса "{course.title}"'
            message = (
                f"Добрый день!\n"
                f'Материалы курса "{course.title}" были обновлены.\n'
                f"Успехов в учебе!"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=recipients,
                fail_silently=False,
            )
        return (
            f"Уведомления отправлены {len(recipients)} подписчикам курса {course.title}"
        )
    except Course.DoesNotExist:
        return "Курс не найден"
