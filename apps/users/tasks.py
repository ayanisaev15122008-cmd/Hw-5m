from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

@shared_task
def calculate_user_stats_task(user_id):
    try:
        user = User.objects.get(id=user_id)
        logger.info(f"Processing stats for user: {user.email}")
        return f"Stats for {user.username} processed successfully."
    except User.DoesNotExist:
        return "User not found"

@shared_task
def send_email_notification_task(subject, message, recipient_list):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False,
    )
    return f"Email sent to {recipient_list}"

@shared_task
def clear_inactive_anonymous_users_task():
    deleted_count, _ = User.objects.filter(is_active=False, last_login__isnull=True).delete()
    return f"Periodic cleanup done. Deleted {deleted_count} inactive users."
