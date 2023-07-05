from Collaborator.models import Collaborator
from Purchase.PurchaseService.generateReports import generate_reports_individual
from Purchase.models import Purchase
from Purchase.models import DeadLine
from datetime import datetime
from datetime import date


def calculates_and_returns_current_referral_spending(employee_who_made_the_purchase:Collaborator):
        """Calcula e retorna o gasto atual com referências de um determinado colaborador.

        Args:
            employee_who_made_the_purchase (Collaborator):
            O colaborador que fez a compra.

        Returns:
            Decimal: O valor total gasto pelo colaborador
            em referências durante o período.
        """
        deadLine = DeadLine.objects.get(id=1).DAY
        today = datetime.now().day
        if today > deadLine:
            start_date = datetime.date(datetime.now().year,
                                       datetime.now().month, (deadLine+1))
            if datetime.now().month+1 == 13:
                end_date = date((datetime.now().year+1), 1, today)
            else: 
                end_date = date(datetime.now().year,
                                (datetime.now().month+1), today)
        else:
            start_date = date(datetime.now().year, (datetime.now().month-1),
                              (deadLine+1))
            end_date = date(datetime.now().year, datetime.now().month, today)
        listPurchases = Purchase.objects.filter(date_purchase__range=(
            start_date, end_date),
            collaborator__cpf=employee_who_made_the_purchase.cpf,
            )
        # total_spended = listPurchases.aggregate(total=Sum('purchaseitem__price'))['total']
        return listPurchases
def calculates_and_returns_last_reference_spend(employee_who_made_the_purchase:Collaborator):
   """Calcula o preço total das compras de um determinado 
    colaborador em um período específico.

    Args:
        employee_who_made_the_purchase (str): Nome do colaborador
        que fez a compra.

    Returns:
        Decimal: O valor total gasto pelo colaborador em referências
        durante o período.
    """
   deadLine = DeadLine.objects.get(id=1).DAY
   today = datetime.now().day
   if today > deadLine:
       start_date = date(datetime.now().year,
                         (datetime.now().month-2), (deadLine+1))
       end_date = date(datetime.now().year,
                       (datetime.now().month-1), deadLine)
   else:
       start_date = date(datetime.now().year,
                         (datetime.now().month-1), (deadLine+1))
       end_date = date(datetime.now().year, datetime.now().month, deadLine)
   try:
       listPurchases = Purchase.objects.filter(date_purchase__range=(
            start_date, end_date),
            collaborator__cpf=employee_who_made_the_purchase.cpf,
            )
   except Exception as e:
        print(f"Exceção ao buscar valores na referencia passada - {e}")
   return listPurchases


def get_data_to_generate_reports(collaborator:Collaborator,start_date,end_date):   
   
   try:
       
       listPurchases = Purchase.objects.filter(date_purchase__range=
                                               (start_date, end_date),collaborator__cpf=collaborator.cpf)
   except Exception as e:
        print(f"Exceção ao buscar as compras para gerar o relatorio - {e}")
   
   return generate_reports_individual(listPurchases,collaborator=collaborator)
