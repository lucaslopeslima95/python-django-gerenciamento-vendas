from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from datetime import datetime
from django.template.loader import get_template
from weasyprint import HTML
import os 


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
    
    
def generate_pdf(nameUser,purchaseItems,total,date,hour):
    template = get_template('emails/confirm_purchase.html')
    context = {'nome':nameUser,'purchaseItems':purchaseItems,'total':total,'date':date,'hour':hour}
    html = template.render(context)
    pdf_file_path = 'comprovante.pdf'  
    HTML(string=html).write_pdf(target=pdf_file_path)
    return pdf_file_path


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
    path_to_pdf = generate_pdf(nameUser,purchaseItems,total,date,hour)
    email.attach_file(path_to_pdf)
    email.attach_alternative(html_content,"text/html")
    email.send()
    delete_pdf(path_to_pdf)
    
    
    
def delete_pdf(path_to_pdf):
    if os.path.exists(path_to_pdf):
        os.remove(path_to_pdf)
        print(f"Arquivo {path_to_pdf} foi excluído com sucesso.")
    else:
        print(f"O arquivo {path_to_pdf} não existe.")




       