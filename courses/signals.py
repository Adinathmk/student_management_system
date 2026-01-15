from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Courses


@receiver(post_delete, sender=Courses)
def notify_admin_course_deleted(sender, instance, **kwargs):
    subject = "Course Deleted"
    message = (
        f"A course has been deleted.\n\n"
        f"Title: {instance.title}\n"
        f"Course Code: {instance.course_code}\n"
        f"Duration: {instance.duration_minutes} minutes\n"
        f"Active: {instance.is_active}"
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_EMAIL],
        fail_silently=False,
    )
