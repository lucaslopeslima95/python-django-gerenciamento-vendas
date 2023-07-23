from Purchase.models import Purchase
from Purchase.models import DeadLine
from datetime import date, datetime
from django.utils import timezone


def current_referral_spending(employee_who_made_the_purchase):
    try:
        list_purchases = []
        deadline = DeadLine.objects.get(id=1).DAY
        today = timezone.now().date()
        current_year = timezone.now().year
        current_month = timezone.now().month

        if today.day > deadline:
            if current_month == 12:
                start_date = timezone.datetime(current_year,
                                               current_month,
                                               deadline + 1).date()
                end_date = timezone.datetime(current_year + 1, 1,
                                             today.day).date()
            else:
                start_date = timezone.datetime(current_year, current_month,
                                               deadline + 1).date()
                end_date = timezone.datetime(current_year, current_month,
                                             today.day).date()
        else:
            start_date = timezone.datetime(current_year, current_month - 1,
                                           deadline + 1).date()
            end_date = timezone.datetime(current_year, current_month,
                                         today.day+1).date()

            list_purchases = Purchase.objects.filter(
                date_purchase__range=(start_date, end_date),
                collaborator__cpf=employee_who_made_the_purchase.cpf)
    except Exception as e:
        print(f"Exceção ao buscar valores na referência Atual - {e}")
    return list_purchases


def last_reference_spend(employee_who_made_the_purchase):
    try:
        listPurchases = []
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
                start_date = date(current_year, current_month - 1,
                                  deadLine + 1)
                end_date = date(current_year, current_month, deadLine)
        else:
            start_date = date(current_year, current_month - 2, deadLine + 1)
            end_date = date(current_year, current_month-1, deadLine)

            listPurchases = Purchase.objects.filter(
                date_purchase__range=(start_date, end_date),
                collaborator__cpf=employee_who_made_the_purchase.cpf)
    except Exception as e:
        print(f"Exceção ao buscar valores na referência passada - {e}")
    return listPurchases
