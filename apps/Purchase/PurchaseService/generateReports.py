from fpdf import FPDF
from django.http import FileResponse
from io import BytesIO
from django.db.models import Sum
from fpdf import FPDF
from django.http import FileResponse
from io import BytesIO
from Purchase.PurchaseService.current_billing import current_billing
from Purchase.models import DeadLine
from datetime import datetime
from datetime import date
from Purchase.models import Purchase


def generate_reports_individual(listPurchases,collaborator):
    print(listPurchases)
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 10)
        pdf.set_fill_color(255, 255, 255)
        pdf.cell(0, 10, f'Relatorio de compras {collaborator.name} ', 1, 1, 'C', 1)
      
        for purchase in listPurchases:
            purchase_date = purchase.date_purchase.strftime('%d/%m/%Y')
            products = purchase.product.all()
            for product in products:
                pdf.cell(0, 10, f"Colaborador: {purchase.collaborator}, Data: {purchase_date},\
                         Produto: {product.name}, Preço: {product.price}", 1, 1, 'L', 1)
       
        try:
            total = listPurchases.aggregate(total=Sum('purchaseitem__price'))['total']
        except Exception as e:
            total = 0.0
            print(f"Exceção ao buscar as compras no periodo definido - {e}")
       
        if total is not None:
            formatted_total = "{:.2f}".format(total)
        else:
            formatted_total = 0.00
      
        pdf.cell(0, 10, f'Total: {formatted_total}', 1, 0, 'C', 1)
  
        pdf_content = pdf.output(dest='S').encode('latin1')
      
        pdf_bytes = BytesIO(pdf_content)
    
    except Exception as e:
        print(f" Exceção ao gerar o relatorio individual {e}")
    
    return FileResponse(pdf_bytes,filename="Relatorio.pdf", as_attachment=True)


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
        end_date = date(datetime.now().year,datetime.now().month,today)
        
    listPurchases = Purchase.objects.filter(date_purchase__range=(start_date, end_date))

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 10)
    pdf.set_fill_color(255, 255, 255)
    pdf.cell(0, 10, 'Vendas Referência Atual', 1, 1, 'C', 1)
    for purchase in listPurchases:
        purchase_date = purchase.date_purchase.strftime('%d/%m/%Y')
        products = purchase.product.all()
        for product in products:
            pdf.cell(0, 9, f"Colaborador: {purchase.collaborator}, Data: {purchase_date},Prod: {product.name}, Preço: {product.price}", 1, 1, 'L', 1)
    total = current_billing()
    formatted_total = "{:.2f}".format(total)
    pdf.cell(0, 10, f'Total: {formatted_total}', 1, 0, 'C', 1)

    pdf_content = pdf.output(dest='S').encode('latin1')
    pdf_bytes = BytesIO(pdf_content)
    return FileResponse(pdf_bytes,filename="Relatorio.pdf",as_attachment=True)