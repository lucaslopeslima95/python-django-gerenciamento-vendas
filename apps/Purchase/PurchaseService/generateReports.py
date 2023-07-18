from datetime import date, datetime
from io import BytesIO

from django.http import FileResponse, HttpResponse
from django.template.loader import get_template
from fpdf import FPDF
from Collaborator.models import Collaborator
from Purchase.models import DeadLine, Purchase
from Purchase.PurchaseService.current_billing import current_billing
from weasyprint import HTML



def generate_reports_individual(collaborator:Collaborator,start_date,end_date):
    
        listPurchases = Purchase.objects.filter(date_purchase__range=
                                               (start_date, end_date),collaborator__cpf=collaborator.cpf)
        generate_at = datetime.now()
        
        context = {
                    'collaborator': collaborator,
                    'listPurchases':listPurchases,
                    'generate_at':generate_at,
                    'end_date':end_date,
                    'start_date':start_date
                }
      
        template = get_template('reports/individual_report.html')
        
        html = template.render(context)
       
        
        response = HttpResponse(content_type='application/pdf')
      
        response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'
        
        HTML(string=html).write_pdf(target=response)

        return response


def generate_reports(request):

    deadLine = DeadLine.objects.get(id=1).DAY
    today = datetime.now().day
    
    if today > deadLine:
        start_date = date(datetime.now().year,datetime.now().month ,(deadLine+1))
        
        if datetime.now().month+1 == 13:
            end_date = date((datetime.now().year+1),1 ,today)
        else: 
            end_date = date(datetime.now().year,(datetime.now().month+1),today)
            
    else:
        start_date = date(datetime.now().year,(datetime.now().month-1) ,(deadLine+1))
        end_date = date(datetime.now().year,datetime.now().month,(today+1))
        
        
    listPurchases = Purchase.objects.filter(date_purchase__range=(start_date, end_date))

    generate_at = datetime.now()
        
    context = {
                'listPurchases':listPurchases,
                'generate_at':generate_at,
                'end_date':end_date,
                'start_date':start_date
            }
    
    template = get_template('reports/current_reffered.html')
    
    html = template.render(context)
    
    
    response = HttpResponse(content_type='application/pdf')
    
    response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'
    
    HTML(string=html).write_pdf(target=response)

    return response