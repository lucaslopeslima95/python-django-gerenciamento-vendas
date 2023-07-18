from django.db.models import Sum
from Purchase.models import DeadLine
from datetime import datetime
from datetime import date
from Purchase.models import Purchase


def current_billing():
    """Calcula o total gasto no período de faturamento atual.

    A função determina o período de faturamento com base na data atual e recupera as compras feitas nesse período.
    Em seguida, calcula o total gasto somando os preços dos itens comprados.

    Returns:
        Decimal: O total gasto no período de faturamento atual.
    """
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
        end_date = date(datetime.now().year,datetime.now().month,today)
        
    listPurchases = Purchase.objects.filter(date_purchase__range=(start_date, end_date))
    total_spended = listPurchases.aggregate(total=Sum('purchaseitem__price'))['total']
    
    return total_spended