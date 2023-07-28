from Collaborator.models import Collaborator
from django.contrib import messages
from django.contrib.auth import authenticate
from django.db.models import F, Sum
from django.shortcuts import redirect, render
from Product.models import Product
from Purchase.models import Purchase, PurchaseItem
from Purchase.PurchaseService.calculateExpends import (
    current_referral_spending, last_reference_spend)
from Purchase.tasks import confirm_purchase
from Stock.models import StoreStock
from User.forms import authForm

from .DTO.PurchaseItemDTO import PurchaseItemDTO
from .forms import searchProductToPurchaseForm
import cv2
from pyzbar.pyzbar import decode


def initial_page_purchase(request):
    cart = PurchaseItemDTO()
    form_code_bar = searchProductToPurchaseForm()
    puchase_list_total_value = None

    if 'sem_produto' not in request.session:
        request.session['sem_produto'] = True

    if request.session['sem_produto']:
        request.session['lista_produtos'] = []
        request.session.save()

    lista_produtos = request.session.get('lista_produtos', [])
    if request.method == "GET":
        try:
            puchase_list_total_value = 0
            for i in lista_produtos:
                puchase_list_total_value += float(i['price'])
        except Exception as e:
            print(f"Exceção ao salvar um colaborador {e}")
            messages.warning(request, "Ocorreu um erro ao adicionar o Produto")

    request.session['sem_produto'] = True
    return render(request, 'purchase/initial_purchase.html', {
                'form_code_bar': form_code_bar,
                'cart': cart,
                'lista_produtos': lista_produtos,
                'total': "R$ {:.2f}".format(puchase_list_total_value),
                'authForm': authForm
                })


def confirm_indentity(request):
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    camera = True
    while camera:
        success, frame = cap.read()
        for code in decode(frame):
            if success:
                cod_auth = code.data.decode('utf-8')
                try:
                    collaborator = Collaborator.objects.get(cod_auth=cod_auth)
                except Exception as e:
                    print(f"Exceção ao buscar o colaborador - {e}")
                camera = False
                cv2.waitKey(1)
                break

        cv2.imshow('Testing-code-scan', frame)
        cv2.waitKey(1)
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(0)

    lista_produtos = request.session.get('lista_produtos', [])
    if collaborator is not None:
        if len(lista_produtos) == 0:
            messages.warning(request, "Nenhum Produto Adicionado")
            return redirect('purchase:initial_page_purchase')
        else:
            if collaborator.active == 1 and save_purchase(
                  request, collaborator):
                messages.success(request, "Salvo com Sucesso.")
                request.session['show_expends'] = True
                current_spend = current_referral_spending(collaborator)
                last_spends = last_reference_spend(collaborator)
                if current_spend:
                    request.session['total_spends_current'] = float(
                       current_spend.aggregate(
                         total=Sum(F('purchaseitem__price') * F(
                             'purchaseitem__quantity')))['total'])
                else:
                    request.session['total_spends_current'] = 0.0
                if last_spends:
                    request.session['spends_last_referred'] = float(
                        last_spends.aggregate(
                            total=Sum(F('purchaseitem__price') * F(
                                'purchaseitem__quantity')))['total'])
                else:
                    request.session['spends_last_referred'] = 0.0
            else:
                messages.warning(request, "Colaborador Inativo")
    else:
        messages.warning(request, "Codigo de barras nao cadastrado")

    return redirect('purchase:initial_page_purchase')


def finish_purchase(request):
    cart = PurchaseItemDTO()
    lista_produtos = request.session.get('lista_produtos', [])
    try:
        if request.method == "POST":
            form = authForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username,
                                    password=password)
                if user is not None:
                    if len(lista_produtos) == 0:
                        messages.warning(request, "Nenhum Produto Adicionado")
                        return redirect('purchase:initial_page_purchase')
                    collaborator = Collaborator.objects.get(user=user.id)
                    if collaborator.active == 1 and save_purchase(
                          request, collaborator):
                        messages.success(request, "Salvo com Sucesso.")
                        request.session['show_expends'] = True
                        current_spend = current_referral_spending(collaborator)
                        last_spends = last_reference_spend(collaborator)
                        if current_spend:
                            request.session['total_spends_current'] = float(
                             current_spend.aggregate(
                                total=Sum(F('purchaseitem__price') * F(
                                    'purchaseitem__quantity')))['total'])

                        else:
                            request.session['total_spends_current'] = 0.0
                        if last_spends:
                            request.session['spends_last_referred'] = float(
                                last_spends.aggregate(
                                    total=Sum(F('purchaseitem__price') * F(
                                        'purchaseitem__quantity')))['total'])
                        else:
                            request.session['spends_last_referred'] = 0.0
                    else:
                        cart.products.clear()
                        messages.warning(request, "Colaborador Inativo")
                        return redirect('purchase:initial_purchase')
                else:
                    messages.warning(request, "Usuario ou Senha Errados.")
                    return redirect('purchase:initial_page_purchase')
            else:
                messages.warning(request, "Credenciais inválidas.")
    except (Exception, Product.DoesNotExist) as e:
        print(f" Exceção ao finalizar a compra - {e}")
    return redirect('purchase:initial_page_purchase')


def confirm_that_there_is_enough(carrinho: list, id):
    try:
        cont = 0
        for i in carrinho:
            if i.product.id == id:
                cont += 1
        stock = StoreStock.objects.get(product__id=id)
        if cont >= stock.stock_quantity:
            return True
        else:
            return False
    except Exception as e:
        print(f"Exceção ao confirmar quantidade de produto no estoque - {e}")


def find_product(request):

    in_cart = PurchaseItemDTO()
    if request.method == "POST":
        product = None
        try:
            form = searchProductToPurchaseForm(request.POST)
            if form.is_valid():
                code_bar = form.cleaned_data['code_bar']
                if code_bar is not None:
                    code_bar_clean = code_bar.replace("-", "").\
                        replace("-", "").replace("-", "")
                    product = Product.objects.get(code_bar=code_bar_clean)
                    if confirm_that_there_is_enough(carrinho=in_cart.products,
                                                    id=product.id):
                        messages.warning(request,
                                         f"O {product.name} \
                                         não possui unidades disponiveis \
                                         no momento")
                    else:

                        request.session['sem_produto'] = False
                        product_dict = {'id': product.pk, 'name': product.name,
                                        'price': str(product.price),
                                        'category': str(product.category)}
                        lista_produtos = request.session.get(
                            'lista_produtos', [])
                        lista_produtos.append(product_dict)
                        request.session['lista_produtos'] = lista_produtos

        except (Product.DoesNotExist, Exception) as e:
            print(f"Exceção ao procurar produto - {e}")
            messages.warning(request, "Produto não encontrado")

    return redirect('purchase:initial_page_purchase')


def remove_product_purchase(request, id):

    lista_produtos = request.session.get('lista_produtos', [])
    lista_produtos.pop(int(id)-1)
    request.session['sem_produto'] = False
    request.session['lista_produtos'] = lista_produtos
    request.session.save()
    return redirect('purchase:initial_page_purchase')


def clean_all_products_purchase(request):
    request.session['lista_produtos'] = []
    request.session.save()
    request.session['total_spends_current'] = 0.0
    request.session['spends_last_referred'] = 0.0
    request.session['show_expends'] = False
    return redirect('purchase:initial_page_purchase')


def save_purchase(request, collaborator: Collaborator) -> bool:
    try:
        lista_produtos = request.session.get('lista_produtos', [])
        purchase_itens = {}
        purchase = Purchase()
        purchase.collaborator = collaborator
        purchase.save()
        for item in lista_produtos:
            if item['name'] not in purchase_itens:
                purchase_itens[item['name']] = {
                    'id': int(item['id']),
                    'price': float(item['price']),
                    'category': str(item['category']),
                    'quantity': 1}
            else:
                purchase_itens[item['name']]['quantity'] += 1

        for product in purchase_itens.items():
            PurchaseItem.objects.create(
                product=Product.objects
                .get(id=product[1]['id']),
                price=product[1]['price'],
                purchase=purchase,
                quantity=product[1]['quantity']
            ).save()

            if not product[1]['category'] == 'Ingressos'\
                    and not product[1]['category'] == 'Camisetas':
                update_quantity(product[1])

        confirm_purchase.delay(email=collaborator.user.email,
                               nameUser=collaborator.name,
                               purchase_itens=purchase_itens)
    except Exception as e:
        print(f" Exceção ao salvar a compra - {e}")
    return True


def update_quantity(product: dict) -> None:
    try:
        stock = StoreStock.objects.get(product__id=product['id'])
        new_quantity = stock.stock_quantity - product['quantity']
        stock.stock_quantity = new_quantity
        stock.save()
    except StoreStock.DoesNotExist:
        print(f"StoreStock não encontrado para o produto com ID {product}")
    except Exception as e:
        print(f"Exceção ao atualizar a quantidade do produto - {e}")


def check_balance(request):
    if request.method == "POST":
        form = authForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                collaborator = Collaborator.objects.get(user=user.id)
                if collaborator.active:
                    current_spends = current_referral_spending(collaborator)
                    last_spends = last_reference_spend(collaborator)

                    if current_spends:
                        request.session['total_spends_current'] = float(
                            current_spends.aggregate(
                                total=Sum(F('purchaseitem__price') * F(
                                    'purchaseitem__quantity')))['total'])

                    else:
                        request.session['total_spends_current'] = 0.0
                    if last_spends:
                        request.session['spends_last_referred'] = float(
                            last_spends.aggregate(
                                total=Sum(F('purchaseitem__price') * F(
                                    'purchaseitem__quantity')))['total'])
                    else:
                        request.session['spends_last_referred'] = 0.0
                    request.session['only_consult'] = True
                else:
                    messages.warning(request, "Perfil de Colaborador Inativo")
            else:
                messages.warning(request, "Credenciais Inválidas")
    return redirect('purchase:initial_page_purchase')


def clean_consult(request):
    request.session['total_spends_current'] = 0.0
    request.session['spends_last_referred'] = 0.0
    request.session['only_consult'] = False
    return redirect('purchase:initial_page_purchase')
