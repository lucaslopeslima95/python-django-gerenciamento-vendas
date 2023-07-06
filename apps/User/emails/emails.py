from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from datetime import datetime




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

def confirm_purchase(email, nameUser,purchaseItems):
    total = None
    for item in purchaseItems:
        total =+ (item.price*item.quantity)
        
    now = datetime.now()
    data_hora_formatada = now.strftime("%d/%m/%Y %H:%M")
    date,hour = data_hora_formatada.split(" ")
    html_content = render_to_string('emails/confirm_purchase.html',{'nome':nameUser,'purchaseItems':purchaseItems,'total':total,'date':date,'hour':hour})
    text_cotent = strip_tags(html_content)
    email = EmailMultiAlternatives(
        'Comprovante de Compras',
        text_cotent,
        settings.EMAIL_HOST_USER,
        [email],
        )
    email.attach_alternative(html_content,"text/html")
    email.send()


