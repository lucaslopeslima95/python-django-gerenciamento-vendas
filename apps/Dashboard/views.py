import calendar
from datetime import date, datetime

from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from Purchase.models import DeadLine, Purchase
from Stock.models import StoreStock, Warehouse


@csrf_protect
@login_required(login_url="login_system")
@user_passes_test(lambda user: user.is_superuser or user.is_staff,
                  login_url='user:page_not_found')
def dashboard(request):
    dias = None
    if request.method == "GET":
        deadLine = DeadLine.objects.get(id=1).DAY
        today = datetime.now().day
        if today > deadLine:
            days_left_next_month = (
                next_month_range()-(next_month_range()-deadLine))
            days_left_current_month = (current_month_range()-today)
            dias = days_left_next_month + days_left_current_month
        else:
            dias = deadLine-today
    return render(request, 'dashboard/dashboard.html', {
            'dias': dias,
            'current_billing': current_billing(),
            'products_low_stock_StoreStock': products_low_stock_StoreStock(),
            'products_low_stock_Warehouse': products_low_stock_Warehouse(),
            })


def products_low_stock_StoreStock():
    return StoreStock.objects.filter(
        stock_quantity__lte=5, product__active=True)


def products_low_stock_Warehouse():
    return Warehouse.objects.filter(stock_quantity__lte=5,
                                    product__active=True)


def current_billing():
    deadLine = DeadLine.objects.get(id=1).DAY
    today = datetime.now().day

    if today > deadLine:
        start_date = date(datetime.now().year,
                          datetime.now().month, (deadLine+1))

        if datetime.now().month+1 == 13:
            end_date = date((datetime.now().year+1), 1, today)
        else:
            end_date = date(datetime.now().year,
                            (datetime.now().month+1), today)

    else:
        start_date = date(datetime.now().year,
                          (datetime.now().month-1), (deadLine+1))
        end_date = date(datetime.now().year, datetime.now().month, today)

    listPurchases = Purchase.objects.filter(
        date_purchase__range=(start_date, end_date))
    total_spended = listPurchases.aggregate(
        total=Sum(
            F('purchaseitem__price') * F('purchaseitem__quantity')))['total']

    return total_spended


def current_month_range():

    current_month = datetime.now().month
    current_year = datetime.now().year
    number_of_days = calendar.monthrange(current_year, current_month)[1]

    return number_of_days


def next_month_range():
    next_month = datetime.now().month
    next_year = datetime.now().year

    if next_month > 12:
        next_month = 1
        next_year += 1

    number_of_days = calendar.monthrange(next_year, (next_month+1))[1]
    return number_of_days
