from Collaborator.models import Collaborator
from Purchase.PurchaseService.generateReports import generate_reports_individual
from Purchase.models import Purchase
from Purchase.models import DeadLine
from datetime import date, datetime
from django.utils import timezone


def calculates_and_returns_current_referral_spending(employee_who_made_the_purchase):

    deadLine = DeadLine.objects.get(id=1).DAY
    today = timezone.now().date().day
    current_year = datetime.now().year
    current_month = datetime.now().month

    if today > deadLine:
        if current_month == 12:
            start_date = date(current_year, current_month, deadLine + 1)
            end_date = date(current_year + 1, 1, today)
        else:
            start_date = date(current_year, current_month, deadLine + 1)
            end_date = date(current_year, current_month, today)
    else:
        start_date = date(current_year, current_month - 1, deadLine + 1)
        end_date = date(current_year, current_month, today)

    listPurchases = Purchase.objects.filter(date_purchase__range=(start_date, end_date),
                                            collaborator__cpf=employee_who_made_the_purchase.cpf)
    return listPurchases
    
def calculates_and_returns_last_reference_spend(employee_who_made_the_purchase):
    deadLine = DeadLine.objects.get(id=1).DAY
    today = timezone.now().date().day
    current_year = datetime.now().year
    current_month = datetime.now().month

    if today > deadLine:
        if current_month == 1:
            start_date = date(current_year - 1, 11, deadLine + 1)
            end_date = date(current_year, 12, deadLine)
        elif current_month == 2:
            start_date = date(current_year, 12, deadLine + 1)
            end_date = date(current_year, current_month - 1, deadLine)
        else:
            start_date = date(current_year, current_month - 1, deadLine + 1)
            end_date = date(current_year, current_month, deadLine)
    else:
        start_date = date(current_year, current_month - 1, deadLine + 1)
        end_date = date(current_year, current_month, deadLine)

    try:
        listPurchases = Purchase.objects.filter(date_purchase__range=(start_date, end_date),
                                                collaborator__cpf=employee_who_made_the_purchase.cpf)
    except Exception as e:
        print(f"Exceção ao buscar valores na referência passada - {e}")

    return listPurchases


def get_data_to_generate_reports(collaborator:Collaborator,start_date,end_date):   
   try: 
       listPurchases = Purchase.objects.filter(date_purchase__range=
                                               (start_date, end_date),collaborator__cpf=collaborator.cpf)
   except Exception as e:
        print(f"Exceção ao buscar as compras para gerar o relatorio - {e}")
   return generate_reports_individual(listPurchases,collaborator=collaborator)


