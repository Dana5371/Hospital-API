from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_activation_code(email, activation_code):

    message = f"""Спасибо за регистрацию.
    Активируйте свой аккаунт по ссылке:
    http://127.0.0.1:8000/v1/api/account/activate/{activation_code}"""
    send_mail(
        'Активация аккаунта',
        message,
        'test@myproject.com',
        [email, ],
        fail_silently=False
    )