from datetime import datetime, date, timedelta
from calendar import month_name, month_abbr

def calculate_purchase_expenses(month):
    # Verifique se o mês é fornecido como número ou nome
    if isinstance(month, int):
        month_number = month
    else:
        month_name = month.lower().capitalize()
        month_number = list(month_name).index(month_name) + 1

    # Obtenha a data de vencimento dinâmica para o mês de referência
    deadline = DeadLine.objects.get(id=1).DAY

    # Obtenha o ano atual
    current_year = datetime.now().year

    # Calcule a data de início e a data de término com base no mês de referência e na data de vencimento
    if month_number > deadline:
        start_date = date(current_year, month_number, deadline + 1)
        if month_number == 12:
            end_date = date(current_year + 1, 1, deadline)
        else:
            end_date = date(current_year, month_number + 1, deadline)
    else:
        if month_number == 1:
            start_date = date(current_year - 1, 12, deadline + 1)
        else:
            start_date = date(current_year, month_number - 1, deadline + 1)
        end_date = date(current_year, month_number, deadline)

    # Filtrar as compras dentro do período calculado
    listPurchases = Purchase.objects.filter(date_purchase__range=(start_date, end_date))

    # Calcular os gastos totais das compras
    total_expenses = listPurchases.aggregate(total=Sum('purchaseitem__price'))['total']
    if total_expenses is None:
        total_expenses = 0

    return total_expenses
