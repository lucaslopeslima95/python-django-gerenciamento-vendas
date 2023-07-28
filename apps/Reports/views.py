from datetime import date, datetime, timedelta

from django.contrib import messages
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.utils import timezone
from Purchase.models import DeadLine, Purchase
from Reports.forms import reportsForm
from weasyprint import HTML


@login_required(login_url="login_system")
@user_passes_test(lambda user: user.is_superuser or user.is_staff,
                  login_url='user:page_not_found')
def page_initial_reports(request):
    return render(request,
                  'reports/page_initial_reports.html',
                  {'form': reportsForm()})


def generate_reports_individual(collaborator, start_date, end_date):

    listPurchases = Purchase.objects.filter(
                date_purchase__range=(start_date, end_date),
                collaborator__cpf=collaborator.cpf)
    total = None
    total = listPurchases.aggregate(
        total=Sum(
            F('purchaseitem__price') * F('purchaseitem__quantity')))['total']
    end_date -= timedelta(days=1)
    generate_at = datetime.now()

    context = {
                'collaborator': collaborator,
                'listPurchases': listPurchases,
                'generate_at': generate_at,
                'end_date': end_date,
                'start_date': start_date,
                'total':float(total)
              }

    template = get_template('reports/template_individual_report.html')

    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'

    HTML(string=html).write_pdf(target=response)

    return response


@login_required(login_url="login_system")
@user_passes_test(lambda user: user.is_superuser or user.is_staff,
                  login_url='user:page_not_found')
def generate_reports(request):

    deadLine = DeadLine.objects.get(id=1).DAY
    today = timezone.datetime.now().day
    current_year = timezone.now().year
    current_month = timezone.now().month

    if today > deadLine:
        start_date = datetime(current_year,
                          current_month,
                          (deadLine+1))

        if current_month+1 == 13:
            end_date = timezone.datetime((current_year+1), 1, today)
        else:
            end_date = timezone.datetime(current_year,
                            (current_month+1), today)

    else:
        start_date = timezone.datetime(current_year,
                          (current_month-1),
                          (deadLine+1))
        end_date = timezone.datetime(current_year,
                        current_month,
                        (today+1))

    start_date = timezone.make_aware(start_date)
    end_date = timezone.make_aware(end_date)
    listPurchases = Purchase.objects.filter(date_purchase__range=(
            start_date, end_date))

    total = None
    total = listPurchases.aggregate(
        total=Sum(
            F('purchaseitem__price') * F('purchaseitem__quantity')))['total']
    generate_at = datetime.now()

    context = {
                'listPurchases': listPurchases,
                'generate_at': generate_at,
                'end_date': end_date,
                'start_date': start_date,
                'total':float(total)
            }

    template = get_template('reports/current_reffered.html')
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'
    HTML(string=html).write_pdf(target=response)

    return response


@user_passes_test(lambda user: user.is_superuser,
                  login_url='user:page_not_found')
@login_required(login_url="login_system")
def make_reports(request):
    try:
        form = reportsForm()
        if request.method == "POST":
            form = reportsForm(request.POST)
            if form.is_valid():
                start_date = form.cleaned_data["start_date"]
                end_date = form.cleaned_data["end_date"]
                if start_date > end_date:
                    messages.warning(request,
                                     "A data de inicio\
                                     deve ser maior que a data de fim")
                    return redirect('reports:page_initial_reports')
                collaborator = form.cleaned_data["collaborator"]
                end_date += timedelta(days=1)

            else:
                messages.error(request, "Formulario Inválido")
                return redirect('reports:page_initial_reports')

    except Exception as e:
        if e is not None:
            print(f"Exceção ao gerar relatório no make reports - {e}")

    return generate_reports_individual(collaborator=collaborator,
                                       start_date=start_date,
                                       end_date=end_date)