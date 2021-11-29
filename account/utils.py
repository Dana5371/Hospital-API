from celery import shared_task
from django.core.mail import send_mail
from hospital_project._celery import app
@app.task
def send_confirmation_code(email, activation_code):

    message = f"""Спасибо за регистрацию.
    Активируйте свой аккаунт по ссылке:
    http://127.0.0.1:3000/v1/api/account/activate/{activation_code}"""
    send_mail(
        'Активация аккаунта',
        message,
        'test@myproject.com',
        [email, ],
        fail_silently=False
    )
    
@app.task
def send_activation_code(user):
    activation_url = f'{user.activation_code}'
    message = f"""Restore password use code: {activation_url}"""
    to_email = user.email
    send_mail(
        'Активация аккаунта',
        message,
        'test@my_project.com',
        [to_email],
        fail_silently=False,
    )
