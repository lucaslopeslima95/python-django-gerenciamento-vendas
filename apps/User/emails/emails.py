from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import send_mail

def confirm_register(email, nameUser):
   
    html_content = render_to_string('emails/email.html',{'nome':nameUser})
    text_cotent = strip_tags(html_content)
    email = EmailMultiAlternatives(
        'Assunto',
        text_cotent,
        settings.EMAIL_HOST_USER,
        [email],
        )
    email.attach_alternative(html_content,"text/html")
    email.attach_file('static_files/imgs/anexo.webp')
    email.send()
    