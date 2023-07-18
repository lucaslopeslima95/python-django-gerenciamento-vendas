
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@shared_task()
def confirm_register(email, nameUser,username,password):
    html_content = render_to_string('emails/welcome.html',{'nome':nameUser,'username':username,'password':password})
    text_cotent = strip_tags(html_content)
    email = EmailMultiAlternatives(
        'Assunto',
        text_cotent,
        settings.EMAIL_HOST_USER,
        [email],
        )
    email.attach_alternative(html_content,"text/html")
    email.send()
    
    




       
