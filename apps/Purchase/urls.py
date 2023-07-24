from django.urls import path
from . import views

app_name = 'purchase'

urlpatterns = [
    path('',
         views.initial_page_purchase,
         name="initial_page_purchase"),
    path('adicionar_produto', views.find_product,
         name="find_product"),
    path('excluir_produto/<int:id>',
         views.remove_product_purchase,
         name="remove_product_purchase"),
    path('limpar_carrinho',
         views.clean_all_products_purchase,
         name="clean_all_products_purchase"),
    path('finalizar_compra',
         views.finish_purchase,
         name="finish_purchase"),
    path('consultar_saldo',
         views.check_balance, name="check_balance"),
    path('limpar_consulta',
         views.clean_consult, name="clean_consult"),
]
