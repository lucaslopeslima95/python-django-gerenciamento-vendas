from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings



def confirm_register(email, nameUser):
   
    html_content = render_to_string('emails/welcome.html',{'nome':nameUser})
    text_cotent = strip_tags(html_content)
    email = EmailMultiAlternatives(
        'Assunto',
        text_cotent,
        settings.EMAIL_HOST_USER,
        [email],
        )
    email.attach_alternative(html_content,"text/html")
    email.send()

def confirm_purchase(email, nameUser,purchaseItems):
    total = None
    for item in purchaseItems:
        total =+ (item.price*item.quantity)
    html_content = render_to_string('emails/confirm_purchase.html',{'nome':nameUser,'purchaseItems':purchaseItems,'total':total})
    text_cotent = strip_tags(html_content)
    email = EmailMultiAlternatives(
        'Comprovante de Compras',
        text_cotent,
        settings.EMAIL_HOST_USER,
        [email],
        )
    email.attach_alternative(html_content,"text/html")
    email.send()


