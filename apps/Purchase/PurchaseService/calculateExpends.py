from datetime import timedelta
from django.utils import timezone
from Purchase.models import DeadLine, Purchase

def current_referral_spending(employee_who_made_the_purchase):
    try:
        list_purchases = []
        deadline = DeadLine.objects.get(id=1).DAY
        today = timezone.now().date()
        current_year = timezone.now().year
        current_month = timezone.now().month
      
        if today.day >= deadline:
            if current_month == 12:
                start_date = timezone.datetime(current_year, current_month, deadline + 1)
                end_date = timezone.datetime(current_year + 1, 1, today.day)
            else:
                start_date = timezone.datetime(current_year, current_month, deadline + 1)
                end_date = timezone.datetime(current_year, current_month, today.day)
        else:
            start_date = timezone.datetime(current_year, current_month - 1, deadline + 1)
            end_date = timezone.datetime(current_year, current_month, today.day + 1)

        start_date = timezone.make_aware(start_date)
        end_date = timezone.make_aware(end_date)

        end_date += timedelta(days=1)
        start_date -= timedelta(days=1)
        list_purchases = Purchase.objects.filter(
            date_purchase__range=(start_date, end_date),
            collaborator__cpf=employee_who_made_the_purchase.cpf)
        end_date -= timedelta(days=1)
        start_date += timedelta(days=1)

    except Exception as e:
        print(f"Exceção ao buscar valores na referência Atual - {e}")
    return list_purchases


def last_reference_spend(employee_who_made_the_purchase):
    try:
        list_purchases = []
        deadline = DeadLine.objects.get(id=1).DAY
        today = timezone.now().date().day
        current_year = timezone.now().year
        current_month = timezone.now().month

        if today >= deadline:
            if current_month == 1:
                start_date = timezone.datetime(current_year - 1, 11, deadline + 1)
                end_date = timezone.datetime(current_year, 12, deadline)
            elif current_month == 2:
                start_date = timezone.datetime(current_year, 12, deadline + 1)
                end_date = timezone.datetime(current_year, current_month - 1, deadline)
            else:
                start_date = timezone.datetime(current_year, current_month - 1, deadline + 1)
                end_date = timezone.datetime(current_year, current_month, deadline)
        else:
            start_date = timezone.datetime(current_year, current_month - 2, deadline + 1)
            end_date = timezone.datetime(current_year, current_month - 1, deadline)

        start_date = timezone.make_aware(start_date)
        end_date = timezone.make_aware(end_date)

        end_date += timedelta(days=1)
        start_date -= timedelta(days=1)
   
        list_purchases = Purchase.objects.filter(
            date_purchase__range=(start_date, end_date),
            collaborator__cpf=employee_who_made_the_purchase.cpf)
        end_date -= timedelta(days=1)
        start_date += timedelta(days=1)
    except Exception as e:
        print(f"Exceção ao buscar valores na referência passada - {e}")
    return list_purchases
